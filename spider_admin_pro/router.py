# -*- coding: utf-8 -*-
from spider_admin_pro.api.action_history_api import action_history_api
from spider_admin_pro.api.auth_api import auth_api
from spider_admin_pro.api.schedule_api import schedule_api
from spider_admin_pro.api.scrapyd_api import scrapyd_api
from spider_admin_pro.api.stats_collection_api import stats_collection_api
from spider_admin_pro.api.system_info_api import system_api

# TODO: 路由集中管理
# 路由配置
ROUTERS = {
    "/api/auth": auth_api,
    "/api/scrapyd": scrapyd_api,
    "/api/schedule": schedule_api,
    "/api/system": system_api,
    "/api/statsCollection": stats_collection_api,
    "/api/actionHistory": action_history_api,
}


def register_blueprint(app):
    for url, blueprint in ROUTERS.items():
        app.register_blueprint(blueprint=blueprint, url_prefix=url)
