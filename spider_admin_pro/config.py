# -*- coding: utf-8 -*-

from environs import Env

env = Env()
env.read_env()

pre_fix = 'SPIDER_ADMIN_PRO_'

with env.prefixed(pre_fix):
    # flask 服务配置
    FLASK_PORT = env.int('PORT', 5000)
    FLASK_HOST = env.str('HOST', '127.0.0.1')

    # 登录账号密码
    BASIC_AUTH_USERNAME = env.str('USERNAME', "admin")
    BASIC_AUTH_PASSWORD = env.str('PASSWORD', "123456")
    BASIC_AUTH_JWT_KEY = "FU0qnuV4t8rr1pvg93NZL3DLn6sHrR1sCQqRzachbo0="

    # token过期时间，单位天
    BASIC_AUTH_EXPIRES = env.int('EXPIRES', 7)

    # scrapyd地址, 结尾不要加斜杆
    SCRAPYD_SERVER = env.str('SCRAPYD', 'http://127.0.0.1:6800')

    # 调度器 调度历史存储设置
    # mysql or sqlite and other, any database for peewee support
    SCHEDULE_HISTORY_DATABASE_URL = env.str('SCHEDULE_HISTORY_DATABASE_URL', 'sqlite:///dbs/schedule_history.db')

    # 调度器 定时任务存储地址
    JOB_STORES_DATABASE_URL = env.str('JOB_STORES_DATABASE_URL', 'sqlite:///dbs/apscheduler.db')
