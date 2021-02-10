# -*- coding: utf-8 -*-

#################################
# env环境变量
#################################

from environs import Env

from spider_admin_pro.config import detault_config

env = Env()
env.read_env()

pre_fix = 'SPIDER_ADMIN_PRO_'

with env.prefixed(pre_fix):
    # flask 服务配置
    FLASK_PORT = env.int('PORT', detault_config.FLASK_PORT)
    FLASK_HOST = env.str('HOST', detault_config.FLASK_HOST)

    # 登录账号密码
    BASIC_AUTH_USERNAME = env.str('USERNAME', detault_config.BASIC_AUTH_USERNAME)
    BASIC_AUTH_PASSWORD = env.str('PASSWORD', detault_config.BASIC_AUTH_PASSWORD)
    BASIC_AUTH_JWT_KEY = env.str('JWT_KEY', detault_config)

    # token过期时间，单位天
    BASIC_AUTH_EXPIRES = env.int('EXPIRES', detault_config.BASIC_AUTH_EXPIRES)

    # scrapyd地址, 结尾不要加斜杆
    SCRAPYD_SERVER = env.str('SCRAPYD', detault_config.SCRAPYD_SERVER)

    # 调度器 调度历史存储设置
    # mysql or sqlite and other, any database for peewee support
    SCHEDULE_HISTORY_DATABASE_URL = env.str('SCHEDULE_HISTORY_DATABASE_URL',
                                            detault_config.SCHEDULE_HISTORY_DATABASE_URL)

    # 调度器 定时任务存储地址
    JOB_STORES_DATABASE_URL = env.str('JOB_STORES_DATABASE_URL', detault_config.JOB_STORES_DATABASE_URL)

    # 日志文件夹
    LOG_DIR = env.str("LOG_DIR", detault_config.LOG_DIR)
