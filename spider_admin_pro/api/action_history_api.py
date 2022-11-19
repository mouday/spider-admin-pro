# -*- coding: utf-8 -*-

"""
行为历史模块
"""
from flask import request

from spider_admin_pro.utils.flask_ext.flask_app import BlueprintAppApi
from spider_admin_pro.service.action_history_service import ActionHistoryService

action_history_api = BlueprintAppApi("action_history_api", __name__)


@action_history_api.post('/loginHistoryList')
def login_history_list():
    page = request.json.get('page', 1)
    size = request.json.get('size', 20)

    rows = ActionHistoryService.get_login_history(
        page=page, size=size
    )
    total = ActionHistoryService.get_login_history_count()

    return {
        'list': rows,
        'total': total
    }
