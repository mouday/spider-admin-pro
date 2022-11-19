# -*- coding: utf-8 -*-

"""
登录模块
"""
from flask import request

from spider_admin_pro.utils.flask_ext.flask_app import BlueprintAppApi
from spider_admin_pro.service.action_history_service import login_history_wrap
from spider_admin_pro.service.auth_service import AuthService

auth_api = BlueprintAppApi("auth", __name__)


@auth_api.post('/login')
@login_history_wrap
def login():
    username = request.json['username']
    password = request.json['password']

    return AuthService.login(
        username=username,
        password=password
    )
