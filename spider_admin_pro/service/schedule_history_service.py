# -*- coding: utf-8 -*-
"""
@File    : schedule_history_service.py
@Date    : 2024-07-18
"""
from spider_admin_pro.model import ScheduleHistoryModel


def get_schedule_history_service_by_job_id(spider_job_id):
    return ScheduleHistoryModel.select().where(
        ScheduleHistoryModel.spider_job_id == spider_job_id
    ).first()