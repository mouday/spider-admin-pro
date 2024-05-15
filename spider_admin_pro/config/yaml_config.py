# -*- coding: utf-8 -*-

#################################
# 读取用户自定义变量
#################################

import os

import yaml

# from spider_admin_pro.logger import logger
from spider_admin_pro.config import default_config

config_file = os.path.join(os.getcwd(), 'config.yml')

# logger.info('config_file: %s', config_file)

if os.path.exists(config_file):
    f = open(config_file, "rb")
    config = yaml.safe_load(f)
    f.close()
else:
    config = {}

# 登录账号密码
BASIC_AUTH_USERNAME = config.get('USERNAME', default_config.BASIC_AUTH_USERNAME)
BASIC_AUTH_PASSWORD = config.get('PASSWORD', default_config.BASIC_AUTH_PASSWORD)
BASIC_AUTH_JWT_KEY = config.get('JWT_KEY', default_config.BASIC_AUTH_JWT_KEY)

# token过期时间，单位天
BASIC_AUTH_EXPIRES = config.get('EXPIRES', default_config.BASIC_AUTH_EXPIRES)

# scrapyd地址, 结尾不要加斜杆
SCRAPYD_SERVER = config.get('SCRAPYD_SERVER', default_config.SCRAPYD_SERVER)

# 调度器 调度历史存储设置
# mysql or sqlite and other, any database for peewee support
SCHEDULE_HISTORY_DATABASE_URL = config.get('SCHEDULE_HISTORY_DATABASE_URL',
                                           default_config.SCHEDULE_HISTORY_DATABASE_URL)

# 调度器 定时任务存储地址
JOB_STORES_DATABASE_URL = config.get('JOB_STORES_DATABASE_URL', default_config.JOB_STORES_DATABASE_URL)

# 日志文件夹
LOG_DIR = config.get("LOG_DIR", default_config.LOG_DIR)

DATABASE_DIR = config.get("DATABASE_DIR", default_config.DATABASE_DIR)

# scrapyd auth
SCRAPYD_USERNAME = config.get("SCRAPYD_USERNAME", None)
SCRAPYD_PASSWORD = config.get("SCRAPYD_PASSWORD", None)
