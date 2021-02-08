# -*- coding: utf-8 -*-
from datetime import datetime

from peewee import CharField, IntegerField, DateTimeField

from spider_admin_pro.model.base import BaseModel


class StatsCollectionModel(BaseModel):
    """运行结果数据收集"""
    id = IntegerField(primary_key=True)

    spider_job_id = CharField(max_length=32)
    project = CharField(max_length=32)
    spider = CharField(max_length=64)

    item_scraped_count = IntegerField()
    item_dropped_count = IntegerField()

    start_time = DateTimeField()
    finish_time = DateTimeField()
    # 持续时间 = finish_time - start_time
    duration = IntegerField()

    finish_reason = CharField(max_length=64)
    log_error_count = IntegerField()

    create_time = DateTimeField(default=datetime.now)


StatsCollectionModel.create_table()

if __name__ == '__main__':
    history = StatsCollectionModel(project="project", spider="baidu", schedule_job_id="1", spider_job_id="1")
    history.save()
