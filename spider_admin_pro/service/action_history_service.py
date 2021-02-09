# -*- coding: utf-8 -*-
from functools import wraps

from flask import request
from ip_area import get_info
from user_agents import parse

from spider_admin_pro.exceptions.api_exception import ApiException
from spider_admin_pro.model.login_history_model import LoginHistoryModel


def login_history_wrap(func):
    """登录日志"""

    @wraps(func)
    def decorator(*args, **kwargs):

        try:
            res = func(*args, **kwargs)
            result = True
        except ApiException as e:
            res = e
            result = False

        username = request.json['username']

        ActionHistoryService.login_history(
            username=username,
            user_agent=request.user_agent.string,
            remote_addr=request.remote_addr,
            result=result
        )

        if result:
            return res
        else:
            raise res

    return decorator


class ActionHistoryService(object):
    """行为记录"""

    @classmethod
    def login_history(cls, username, user_agent, remote_addr, result):
        ua = parse(user_agent)

        # 登录日志
        LoginHistoryModel.create(
            username=username,
            ip=remote_addr,
            address=cls.get_address(remote_addr),
            user_agent=user_agent,
            system=ua.os.family,
            browser=ua.browser.family,
            version=ua.browser.version_string,
            result=result
        )

    @classmethod
    def get_address(cls, ip):
        """获取ip地址信息"""
        info = get_info(ip)

        country = info['country']
        region = info['region']
        city = info['city']
        isp = info['isp']

        return f'{country} {region} {city} {isp}'

    @classmethod
    def get_login_history(cls, page=1, size=20):
        rows = (LoginHistoryModel
                .select()
                .order_by(LoginHistoryModel.create_time.desc())
                .paginate(page, size).dicts())

        return rows

    @classmethod
    def get_login_history_count(cls):
        return LoginHistoryModel.select().count()
