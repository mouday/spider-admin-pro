# -*- coding: utf-8 -*-

import logging
from logging.handlers import RotatingFileHandler
from peewee import *
from playhouse.db_url import connect, register_database
from playhouse.shortcuts import ReconnectMixin
from playhouse.sqliteq import SqliteQueueDatabase

from spider_admin_pro.config import SCHEDULE_HISTORY_DATABASE_URL, resolve_log_file
from spider_admin_pro.utils.sqlite_util import make_sqlite_dir

# 显示查询日志
peewee_logger = logging.getLogger('peewee')
peewee_logger.setLevel(logging.DEBUG)

# file_handler = logging.FileHandler(resolve_log_file('peewee.log'))
file_handler = RotatingFileHandler(
    filename=resolve_log_file('peewee.log'),
    maxBytes=1024 * 1024 * 1,  # 1MB
    backupCount=1,
    encoding='utf-8'
)
peewee_logger.addHandler(file_handler)


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
