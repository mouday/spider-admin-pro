# -*- coding: utf-8 -*-
"""
@File    : system_task_service.py
@Date    : 2024-04-01
"""
from apscheduler.schedulers.background import BackgroundScheduler

from spider_admin_pro.model.base import db
from spider_admin_pro.service.schedule_service import ScheduleService
from spider_admin_pro.service.stats_collection_service import StatsCollectionService
from spider_admin_pro.logger import logger


def start_system_scheduler():
    logger.info("system_scheduler start")

    scheduler = BackgroundScheduler()

    # 方式二：cron 定时任务 1 1 * * *
    scheduler.add_job(remove_history_log_task, 'cron', minute="1", hour="1", day="*", month="*", day_of_week="*")

    scheduler.start()


@db.connection_context()
def remove_history_log_task():
    """
    移除历史日志，默认保留近7天
    :return:
    """
    ScheduleService.remove_history_log()

    StatsCollectionService.remove_history_log()
