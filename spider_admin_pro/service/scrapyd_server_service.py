# -*- coding: utf-8 -*-
"""
@File    : scrapyd_server_service.py
@Date    : 2024-07-13
"""
from spider_admin_pro.model import ScrapydServerModel


def get_available_scrapyd_server_count():
    """
    获取可用服务的数量
    :return:
    """
    return ScrapydServerModel.select().where(
        ScrapydServerModel.status == 1
    ).count()


def get_available_scrapyd_server():
    """
    获取一个随机可用服务
    :return:
    """
    return ScrapydServerModel.select().where(
        ScrapydServerModel.status == 1
    ).order_by(
        ScrapydServerModel.last_time.asc()
    ).first()


def get_available_scrapyd_server_by_id(scrapyd_server_id):
    """
    获取一个指定的可用服务
    :param scrapyd_server_id:
    :return:
    """
    return ScrapydServerModel.select().where(
        ScrapydServerModel.id == scrapyd_server_id,
        ScrapydServerModel.status == 1
    ).first()
