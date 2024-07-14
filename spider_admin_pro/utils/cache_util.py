# -*- coding: utf-8 -*-
"""
@File    : cache_util.py
@Date    : 2024-07-13
"""
import os

from spider_admin_pro.config import CACHE_DIR


def get_cache(filename, default_value=''):
    fullname = os.path.join(CACHE_DIR, filename)
    value = default_value

    if os.path.exists(fullname):
        with open(fullname, 'r') as f:
            value = f.read()
    else:
        with open(fullname, 'w') as f:
            f.write(default_value)

    return value
