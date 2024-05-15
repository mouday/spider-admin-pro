# -*- coding: utf-8 -*-

from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix

from spider_admin_pro.router import register_blueprint
from spider_admin_pro.service import system_task_service
from spider_admin_pro.utils.flask_ext.flask_app import FlaskApp
from spider_admin_pro.utils.statics import compress_statics
from spider_admin_pro.logger import logger
from flask_compress import Compress
from whitenoise import WhiteNoise
import importlib.resources as R

static_dir = str(R.files("spider_admin_pro") / "public")
# 静态文件预压缩
logger.info("开始静态文件预压缩")
compress_statics(static_dir)
logger.info("结束静态文件预压缩")
app = FlaskApp(__name__, static_folder=None, template_folder=None)
# 为wsgi接口响应添加压缩功能
Compress(app)
# 跨域支持
CORS(app, supports_credentials=True, max_age=6000)
# 静态文件服务
app.wsgi_app = WhiteNoise(ProxyFix(app.wsgi_app), root=static_dir, index_file=True)
# 注册路由
register_blueprint(app)


# 启动系统后台任务
system_task_service.start_system_scheduler()
