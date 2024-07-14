# -*- coding: utf-8 -*-

from .login_history_model import LoginHistoryModel
from .schedule_history_model import ScheduleHistoryModel
from .scrapyd_server_model import ScrapydServerModel
from .stats_collection_model import StatsCollectionModel

tables = [
    LoginHistoryModel,
    ScheduleHistoryModel,
    StatsCollectionModel,
    ScrapydServerModel
]

for table in tables:
    if not table.table_exists():
        table.create_table()
