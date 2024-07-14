# -*- coding: utf-8 -*-
"""
@File    : schedule_type_enum.py
@Date    : 2024-07-14
"""


class ScheduleTypeEnum(object):
    # 指定一个服务器
    ONLY_ONE_SERVER = '0'

    # 随机轮询
    RANDOM_SERVER = '1'

    LIST_SERVER = '2'
