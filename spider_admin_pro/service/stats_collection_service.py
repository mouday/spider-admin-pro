# -*- coding: utf-8 -*-

"""
spider运行结果数据收集模块
"""

from spider_admin_pro.model.stats_collection_model import StatsCollectionModel
from spider_admin_pro.utils.time_util import TimeUtil


class StatsCollectionService(object):
    @classmethod
    def list(cls, page=1, size=20, project=None, spider=None):
        query = StatsCollectionModel.select()

        if project:
            query = query.where(StatsCollectionModel.project == project)

        if spider:
            query = query.where(StatsCollectionModel.spider == spider)

        rows = (query
                .order_by(StatsCollectionModel.create_time.desc())
                .paginate(page, size)
                .dicts()
                )

        # 计算持续时间
        for row in rows:
            row['duration_str'] = TimeUtil.format_duration((row['finish_time'] - row['start_time']).seconds)

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
