# -*- coding: utf-8 -*-

# flask 服务配置
FLASK_PORT = 5000
FLASK_HOST = '127.0.0.1'

# 登录账号密码
BASIC_AUTH_USERNAME = "admin"
BASIC_AUTH_PASSWORD = "123456"
BASIC_AUTH_JWT_KEY = "ooxx"

# token过期时间，单位天
BASIC_AUTH_EXPIRES = 7

# scrapyd地址
SCRAPYD_SERVER = 'http://127.0.0.1:6800'

# 调度器 调度历史存储设置
# mysql or sqlite and other, any database for peewee support
SCHEDULE_HISTORY_DATABASE_URL = 'sqlite:///dbs/schedule_history.db'

# 调度器 定时任务存储地址
APSCHEDULER_DATABASE_URL = 'sqlite:///dbs/apscheduler.db'
