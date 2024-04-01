# -*- coding: utf-8 -*-
import json
import logging
import uuid
from datetime import datetime, timedelta
from logging.handlers import RotatingFileHandler

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler

from spider_admin_pro.config import JOB_STORES_DATABASE_URL, resolve_log_file
from spider_admin_pro.model.schedule_history_model import ScheduleHistoryModel
from spider_admin_pro.service.scrapyd_service import ScrapydService
from spider_admin_pro.service.stats_collection_service import StatsCollectionService
from spider_admin_pro.utils.sqlite_util import make_sqlite_dir
from spider_admin_pro.utils.time_util import TimeUtil

apscheduler_logger = logging.getLogger('apscheduler')

# file_handler = logging.FileHandler(resolve_log_file('apscheduler.log'))
file_handler = RotatingFileHandler(
    filename=resolve_log_file('apscheduler.log'),
    maxBytes=1024 * 1024 * 1,  # 1MB
    backupCount=1,
    encoding='utf-8'
)

apscheduler_logger.addHandler(file_handler)

# ==============================================
# 调度器服务配置
# ==============================================

make_sqlite_dir(JOB_STORES_DATABASE_URL)

JOBSTORES = {
    'default': SQLAlchemyJobStore(url=JOB_STORES_DATABASE_URL)
}

JOB_DEFAULTS = {
    'misfire_grace_time': None,
    'coalesce': True,
    'max_instances': 1
}

scheduler = BackgroundScheduler(jobstores=JOBSTORES, job_defaults=JOB_DEFAULTS)

scheduler.start()


class ScheduleService(object):

    @classmethod
    def add_job(cls, project, spider, cron, job_id=None, options=None):
        # 必传参数校验
        if not project:
            raise Exception('project is null')

        if not spider:
            raise Exception('spider is null')

        # 处理cron表达式
        crons = cron.split(' ')

        crons = filter(lambda x: x, crons)

        minute, hour, day, month, day_of_week = crons

        # 可选参数处理
        if options:
            opt = json.loads(options)

            if not isinstance(opt, dict):
                raise Exception("options参数的json数据不能解析为字典dict对象")

        if job_id is None:
            job_id = cls.get_job_id()

        kwargs = {
            'project': project,
            'spider': spider,
            'cron': cron,
            'options': options,
            'schedule_job_id': job_id
        }

        scheduler.add_job(
            func=ScrapydService.run_spider,
            trigger='cron',
            id=job_id,
            minute=minute, hour=hour, day=day, month=month, day_of_week=day_of_week,
            replace_existing=True,
            kwargs=kwargs)

    @classmethod
    def get_job_id(cls):
        """spider_job_id"""
        return uuid.uuid4().hex

    @classmethod
    def get_log_list(cls, page=1, size=20,
                     status=None,
                     project=None,
                     spider=None,
                     schedule_job_id=None):
        """调度日志列表"""

        query = ScheduleHistoryModel.select()

        if project:
            query = query.where(ScheduleHistoryModel.project == project)
        if spider:
            query = query.where(ScheduleHistoryModel.spider == spider)
        if schedule_job_id:
            query = query.where(ScheduleHistoryModel.schedule_job_id == schedule_job_id)

        if status == 'success':
            query = query.where(ScheduleHistoryModel.spider_job_id != '')
        elif status == 'error':
            query = query.where(ScheduleHistoryModel.spider_job_id == '')

        rows = query.order_by(
            ScheduleHistoryModel.create_time.desc()
        ).paginate(page, size).dicts()

        return list(rows)

    @classmethod
    def get_log_list_with_stats(cls, page=1, size=20,
                                status=None,
                                project=None,
                                spider=None,
                                schedule_job_id=None):
        """获取调度日志和运行日志"""

        rows = cls.get_log_list(
            page=page, size=size, status=status,
            project=project, spider=spider,
            schedule_job_id=schedule_job_id
        )

        # 关联schedule
        spider_job_ids = []

        for row in rows:
            # 调度状态
            if row['spider_job_id'] != '':
                spider_job_ids.append(row['spider_job_id'])
                row['status'] = True
            else:
                row['status'] = False

            # 调度模式
            if row['schedule_job_id']:
                row['schedule_mode'] = '自动'
            else:
                row['schedule_mode'] = '手动'

        stats_dict = StatsCollectionService.get_dict_by_spider_job_ids(spider_job_ids)

        # 运行状态
        for row in rows:
            spider_job_id = row['spider_job_id']

            if spider_job_id in stats_dict:
                stats_row = stats_dict[spider_job_id]
                row['run_status'] = 'finished'
                row['item_count'] = stats_row['item_dropped_count'] + stats_row['item_scraped_count']
                row['log_error_count'] = stats_row['log_error_count']
                row['duration_str'] = TimeUtil.format_duration(stats_row['duration'])
            else:
                row['run_status'] = 'unknown'
        return rows

    @classmethod
    def get_log_total_count(cls, project=None, spider=None, schedule_job_id=None):
        """计算日志总条数"""
        query = ScheduleHistoryModel.select()

        if project:
            query = query.where(ScheduleHistoryModel.project == project)

        if spider:
            query = query.where(ScheduleHistoryModel.spider == spider)

        if schedule_job_id:
            query = query.where(ScheduleHistoryModel.schedule_job_id == schedule_job_id)

        return query.count()

    @classmethod
    def get_log_success_count(cls, project=None, spider=None, schedule_job_id=None):
        """计算成功日志条数"""
        query = ScheduleHistoryModel.select()

        if project:
            query = query.where(ScheduleHistoryModel.project == project)

        if spider:
            query = query.where(ScheduleHistoryModel.spider == spider)

        if schedule_job_id:
            query = query.where(ScheduleHistoryModel.schedule_job_id == schedule_job_id)

        query = query.where(ScheduleHistoryModel.spider_job_id != '')
        return query.count()

    @classmethod
    def get_log_error_count(cls, project=None, spider=None, schedule_job_id=None):
        """计算失败日志条数"""
        query = ScheduleHistoryModel.select()

        if project:
            query = query.where(ScheduleHistoryModel.project == project)

        if spider:
            query = query.where(ScheduleHistoryModel.spider == spider)

        if schedule_job_id:
            query = query.where(ScheduleHistoryModel.schedule_job_id == schedule_job_id)

        query = query.where(ScheduleHistoryModel.spider_job_id == '')
        return query.count()

    @classmethod
    def remove_log(cls, project=None, spider=None, schedule_job_id=None, status=None):
        """移除日志"""
        query = ScheduleHistoryModel.delete()

        if project:
            query = query.where(ScheduleHistoryModel.project == project)

        if spider:
            query = query.where(ScheduleHistoryModel.spider == spider)

        if schedule_job_id:
            query = query.where(ScheduleHistoryModel.schedule_job_id == schedule_job_id)

        if status == 'success':
            query = query.where(ScheduleHistoryModel.spider_job_id != '')
        elif status == 'error':
            query = query.where(ScheduleHistoryModel.spider_job_id == '')

        return query.execute()

    @classmethod
    def remove_history_log(cls, days=7):
        """移除历史日志"""
        max_datetime = datetime.now() - timedelta(days=days)

        query = ScheduleHistoryModel.delete().where(
            ScheduleHistoryModel.create_time <= max_datetime
        )

        return query.execute()
