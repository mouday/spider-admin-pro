# -*- coding: utf-8 -*-

"""
登录模块
"""
from flask import request

from spider_admin_pro.lib.flask_app.flask_app import BlueprintAppApi
from spider_admin_pro.service.auth import AuthService

auth_api = BlueprintAppApi("auth", __name__)


@auth_api.post('/login')
def login():
    username = request.json['username']
    password = request.json['password']

    return AuthService.login(username=username, password=password)
