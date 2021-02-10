# -*- coding: utf-8 -*-
from datetime import datetime

from peewee import CharField, IntegerField, DateTimeField

from spider_admin_pro.model.base import BaseModel


class ScheduleHistoryModel(BaseModel):
    """调度历史存储"""
    id = IntegerField(primary_key=True)

    project = CharField(max_length=32)
    spider = CharField(max_length=64)
    spider_job_id = CharField(max_length=32)
    options = CharField()
    message = CharField()

    schedule_job_id = CharField(max_length=32)

    create_time = DateTimeField(default=datetime.now)

    @classmethod
    def insert_row(cls, project, spider, schedule_job_id=None, options=None, spider_job_id=None, message=None):
        # 统一处理为字符串
        if not schedule_job_id:
            schedule_job_id = ''

        if not options:
            options = ''

        if not spider_job_id:
            spider_job_id = ''

        if not message:
            message = ''

        cls.create(
            project=project,
            spider=spider,
            spider_job_id=spider_job_id,
            options=options,
            schedule_job_id=schedule_job_id,
            message=message
        )
