# -*- coding: utf-8 -*-
from flask import request, make_response
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix

from spider_admin_pro.router import register_blueprint
from spider_admin_pro.service import system_task_service
from spider_admin_pro.utils.flask_ext.flask_app import FlaskApp

app = FlaskApp(__name__, static_folder=None)
CORS(app, supports_credentials=True)
app.wsgi_app = ProxyFix(app.wsgi_app)

# 注册路由
register_blueprint(app)


@app.before_request
def before_request():
    """跨域请求会出现options，直接返回即可"""
    if request.method == 'OPTIONS':
        return make_response()


# 启动系统后台任务
system_task_service.start_system_scheduler()
