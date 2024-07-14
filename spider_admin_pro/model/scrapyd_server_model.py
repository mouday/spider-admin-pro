# -*- coding: utf-8 -*-
"""
scrapyd_server_model.py
"""
from datetime import datetime

from peewee import CharField, IntegerField, DateTimeField
from playhouse.shortcuts import model_to_dict

from spider_admin_pro.model.base import BaseModel


class ScrapydServerModel(BaseModel):
    """scrapyd 配置"""
    id = IntegerField(primary_key=True)

    server_url = CharField()
    # 别名
    server_name = CharField(default="")

    username = CharField(default="")
    password = CharField(default="")

    status = IntegerField(default=0)

    # 最后提交任务的时间
    last_time = DateTimeField(default=datetime.now)

    create_time = DateTimeField(default=datetime.now)
    update_time = DateTimeField(default=datetime.now)

    def to_dict(self):
        return model_to_dict(self)
