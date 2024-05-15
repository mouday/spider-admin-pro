# -*- coding: utf-8 -*-
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix

from spider_admin_pro.router import register_blueprint
from spider_admin_pro.service import system_task_service
from spider_admin_pro.utils.flask_ext.flask_app import FlaskApp
from flask_compress import Compress
from whitenoise import WhiteNoise
import importlib.resources as R

app = FlaskApp(__name__, static_folder=None, template_folder=None)

# 中间件、wsgi_app、静态文件处理
Compress(app)
CORS(app, supports_credentials=True, max_age=6000)
static_dir = R.files("spider_admin_pro") / "public"
app.wsgi_app = WhiteNoise(ProxyFix(app.wsgi_app), root=str(static_dir), index_file=True)

# 注册路由
register_blueprint(app)


# 启动系统后台任务
system_task_service.start_system_scheduler()
