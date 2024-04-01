# -*- coding: utf-8 -*-

"""
spider运行结果数据收集模块
"""
from datetime import datetime, timedelta

from spider_admin_pro.model.stats_collection_model import StatsCollectionModel
from spider_admin_pro.utils.time_util import TimeUtil


class StatsCollectionService(object):
    @classmethod
    def list(cls, page=1, size=20,
             project=None, spider=None,
             order_prop=None, order_type=None
             ):
        """

        :param page:
        :param size:
        :param project:
        :param spider:
        :param order_prop: duration, log_error_count
        :param order_type: descending, ascending
        :return:
        """
        query = StatsCollectionModel.select()

        # 查询条件
        if project:
            query = query.where(StatsCollectionModel.project == project)

        if spider:
            query = query.where(StatsCollectionModel.spider == spider)

        # 排序, 默认创建时间倒排
        if order_prop == 'duration':
            if order_type == 'descending':
                query = query.order_by(StatsCollectionModel.duration.desc())
            else:
                query = query.order_by(StatsCollectionModel.duration.asc())

        elif order_prop == 'log_error_count':
            if order_type == 'descending':
                query = query.order_by(StatsCollectionModel.log_error_count.desc())
            else:
                query = query.order_by(StatsCollectionModel.log_error_count.asc())

        else:
            query = query.order_by(StatsCollectionModel.create_time.desc())

        # 分页
        rows = query.paginate(page, size).dicts()

        # 计算持续时间
        for row in rows:
            row['duration_str'] = TimeUtil.format_duration(row['duration'])

        return rows

    @classmethod
    def count(cls, project=None, spider=None):
        query = StatsCollectionModel.select()

        if project:
            query = query.where(StatsCollectionModel.project == project)

        if spider:
            query = query.where(StatsCollectionModel.spider == spider)

        return query.count()

    @classmethod
    def delete(cls, project=None, spider=None):
        query = StatsCollectionModel.delete()

        if project:
            query = query.where(StatsCollectionModel.project == project)

        if spider:
            query = query.where(StatsCollectionModel.spider == spider)

        return query.execute()

    @classmethod
    def get_dict_by_spider_job_ids(cls, spider_job_ids):
        rows = (StatsCollectionModel
                .select()
                .where(StatsCollectionModel.spider_job_id.in_(spider_job_ids))
                .dicts())
        dct = {}
        for row in rows:
            dct[row['spider_job_id']] = row

        return dct

    @classmethod
    def remove_history_log(cls, days=7):
        """移除历史日志"""
        max_datetime = datetime.now() - timedelta(days=days)

        query = StatsCollectionModel.delete().where(
            StatsCollectionModel.create_time <= max_datetime
        )

        return query.execute()
