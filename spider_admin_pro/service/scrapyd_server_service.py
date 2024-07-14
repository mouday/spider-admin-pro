# -*- coding: utf-8 -*-
"""
@File    : scrapyd_server_service.py
@Date    : 2024-07-13
"""
from spider_admin_pro.model import ScrapydServerModel


def get_available_scrapyd_server():
    return ScrapydServerModel.select().where(
        ScrapydServerModel.status == 1
    ).order_by(
        ScrapydServerModel.last_time.asc()
    ).first()


def get_available_scrapyd_server_by_id(scrapyd_server_id):
    return ScrapydServerModel.select().where(
        ScrapydServerModel.id == scrapyd_server_id,
        ScrapydServerModel.status == 1
    ).first()
