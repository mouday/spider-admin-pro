# -*- coding: utf-8 -*-

import logging

from peewee import *
from playhouse.db_url import connect, register_database
from playhouse.shortcuts import ReconnectMixin
from playhouse.sqliteq import SqliteQueueDatabase

from spider_admin_pro.config import SCHEDULE_HISTORY_DATABASE_URL
# 显示查询日志
from spider_admin_pro.utils.sqlite_util import make_sqlite_dir

logger = logging.getLogger('peewee')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


class ReconnectSqliteDatabase(ReconnectMixin, SqliteQueueDatabase):
    pass


class ReconnectMySQLDatabase(ReconnectMixin, MySQLDatabase):
    pass


register_database(ReconnectSqliteDatabase, 'sqlite')
register_database(ReconnectMySQLDatabase, 'mysql')

make_sqlite_dir(SCHEDULE_HISTORY_DATABASE_URL)
db = connect(url=SCHEDULE_HISTORY_DATABASE_URL)


class BaseModel(Model):
    class Meta:
        database = db
