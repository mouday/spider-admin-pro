# -*- coding: utf-8 -*-
import json
import uuid

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler

from spider_admin_pro.config import JOB_STORES_DATABASE_URL
from spider_admin_pro.logger import Logger
from spider_admin_pro.model.history import HistoryModel
from spider_admin_pro.service.scrapyd_service import ScrapydService
from spider_admin_pro.utils.sqlite_util import make_sqlite_dir

logger = Logger.get_logger('apscheduler')

# ==============================================
# 调度器服务配置
# ==============================================

make_sqlite_dir(JOB_STORES_DATABASE_URL)

JOBSTORES = {
    'default': SQLAlchemyJobStore(url=JOB_STORES_DATABASE_URL)
}

JOB_DEFAULTS = {
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
        return uuid.uuid4().hex

    @classmethod
    def get_log_list(cls, page=1, size=20, status=None, project=None, spider=None, schedule_job_id=None):
        query = HistoryModel.select()

        if project:
            query = query.where(HistoryModel.project == project)
        if spider:
            query = query.where(HistoryModel.spider == spider)
        if schedule_job_id:
            query = query.where(HistoryModel.schedule_job_id == schedule_job_id)

        if status == 'success':
            query = query.where(HistoryModel.spider_job_id != '')
        elif status == 'error':
            query = query.where(HistoryModel.spider_job_id == '')

        query = query.order_by(
            HistoryModel.create_time.desc()
        ).paginate(page, size).dicts()

        lst = []
        for row in query:
            row['status'] = False if row['spider_job_id'] == '' else True
            lst.append(row)

        return lst

    @classmethod
    def get_log_total_count(cls, project=None, spider=None, schedule_job_id=None):
        query = HistoryModel.select()

        if project:
            query = query.where(HistoryModel.project == project)

        if spider:
            query = query.where(HistoryModel.spider == spider)

        if schedule_job_id:
            query = query.where(HistoryModel.schedule_job_id == schedule_job_id)

        return query.count()

    @classmethod
    def get_log_success_count(cls, project=None, spider=None, schedule_job_id=None):
        query = HistoryModel.select()

        if project:
            query = query.where(HistoryModel.project == project)

        if spider:
            query = query.where(HistoryModel.spider == spider)

        if schedule_job_id:
            query = query.where(HistoryModel.schedule_job_id == schedule_job_id)

        query = query.where(HistoryModel.spider_job_id != '')
        return query.count()

    @classmethod
    def get_log_error_count(cls, project=None, spider=None, schedule_job_id=None):
        query = HistoryModel.select()

        if project:
            query = query.where(HistoryModel.project == project)

        if spider:
            query = query.where(HistoryModel.spider == spider)

        if schedule_job_id:
            query = query.where(HistoryModel.schedule_job_id == schedule_job_id)

        query = query.where(HistoryModel.spider_job_id == '')
        return query.count()

    @classmethod
    def remove_log(cls, project=None, spider=None, schedule_job_id=None, status=None):
        query = HistoryModel.delete()

        if project:
            query = query.where(HistoryModel.project == project)

        if spider:
            query = query.where(HistoryModel.spider == spider)

        if schedule_job_id:
            query = query.where(HistoryModel.schedule_job_id == schedule_job_id)

        if status == 'success':
            query = query.where(HistoryModel.spider_job_id != '')
        elif status == 'error':
            query = query.where(HistoryModel.spider_job_id == '')

        return query.execute()


if __name__ == '__main__':
    print(SchedulerService.get_log_list(1, 20, 'success', 'project', 'spider'))
