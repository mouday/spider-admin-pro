# -*- coding: utf-8 -*-

import logging

from peewee import *
from playhouse.shortcuts import ReconnectMixin
from playhouse.sqliteq import SqliteQueueDatabase

from spider_admin_pro.config import (
    SCHEDULE_DATABASE_SCHEME,
    SCHEDULE_DATABASE_NAME,
    SCHEDULE_DATABASE_USER,
    SCHEDULE_DATABASE_PASSWORD,
    SCHEDULE_DATABASE_HOST,
    SCHEDULE_DATABASE_PORT
)

# 显示查询日志
logger = logging.getLogger('peewee')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


class ReconnectSqliteDatabase(ReconnectMixin, SqliteQueueDatabase):
    pass


class ReconnectMySQLDatabase(ReconnectMixin, MySQLDatabase):
    pass


if SCHEDULE_DATABASE_SCHEME == 'sqlite':
    db = ReconnectSqliteDatabase(database=SCHEDULE_DATABASE_NAME)

elif SCHEDULE_DATABASE_SCHEME == 'mysql':
    db = ReconnectMySQLDatabase(
        database=SCHEDULE_DATABASE_NAME,
        user=SCHEDULE_DATABASE_USER,
        password=SCHEDULE_DATABASE_PASSWORD,
        host=SCHEDULE_DATABASE_HOST,
        port=SCHEDULE_DATABASE_PORT
    )
else:
    raise Exception('not support database scheme')


class BaseModel(Model):
    class Meta:
        database = db
