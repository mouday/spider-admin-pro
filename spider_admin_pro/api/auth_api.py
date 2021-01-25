# -*- coding: utf-8 -*-

"""
登录模块
"""
from flask import request

from spider_admin_pro.flask_app import BlueprintAppApi
from spider_admin_pro.service.auth_service import AuthService

auth_api = BlueprintAppApi("auth", __name__)


@auth_api.post('/login')
def login():
    username = request.json['username']
    password = request.json['password']

    return AuthService.login(username=username, password=password)
