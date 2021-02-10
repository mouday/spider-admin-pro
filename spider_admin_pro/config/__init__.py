# -*- coding: utf-8 -*-

"""
配置优先级：默认 < env环境变量 < yaml配置文件
"""

from .yaml_config import *

if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)


def resolve_log_file(filename):
    """补全日志文件夹"""
    return os.path.join(LOG_DIR, filename)
