# -*- coding: utf-8 -*-
from flask import request, make_response
from flask_cors import CORS

from spider_admin_pro.api.auth import auth_api
from spider_admin_pro.api.schedule import schedule_api
from spider_admin_pro.api.scrapyd import scrapyd_api
from spider_admin_pro.api.system_info import system_api
from spider_admin_pro.lib.flask_app.flask_app import FlaskApp
from spider_admin_pro.web.main import web

app = FlaskApp(__name__, static_folder=None)
CORS(app, supports_credentials=True)

app.register_blueprint(web, url_prefix="/")
app.register_blueprint(auth_api, url_prefix="/api/auth")
app.register_blueprint(scrapyd_api, url_prefix="/api/scrapyd")
app.register_blueprint(schedule_api, url_prefix="/api/schedule")
app.register_blueprint(system_api, url_prefix="/api/system")


@app.before_request
def before_request():
    if request.method == 'OPTIONS':
        return make_response()
