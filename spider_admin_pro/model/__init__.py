# -*- coding: utf-8 -*-

from .login_history_model import LoginHistoryModel
from .schedule_history_model import ScheduleHistoryModel
from .stats_collection_model import StatsCollectionModel

tables = [
    LoginHistoryModel,
    ScheduleHistoryModel,
    StatsCollectionModel
]

for table in tables:
    if not table.table_exists():
        table.create_table()
