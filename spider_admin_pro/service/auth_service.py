# -*- coding: utf-8 -*-

from flask import current_app

from spider_admin_pro.config import (
    BASIC_AUTH_USERNAME,
    BASIC_AUTH_PASSWORD,
    BASIC_AUTH_JWT_KEY,
    BASIC_AUTH_EXPIRES
)
from spider_admin_pro.exceptions.api_exception import ApiException
from spider_admin_pro.exceptions.constant import TOKEN_INVALID_ERROR, USERNAME_OR_PASSWORD_ERROR
from spider_admin_pro.utils.jwt_util import JwtUtil

jwt_util = JwtUtil(key=BASIC_AUTH_JWT_KEY)


class AuthService(object):
    # 用户名、密码
    username = BASIC_AUTH_USERNAME
    password = BASIC_AUTH_PASSWORD

    # 过期时间
    expires = BASIC_AUTH_EXPIRES

    @classmethod
    def login(cls, username, password):
        if username == cls.username and password == cls.password:
            # 7天有效
            token = jwt_util.encode(
                payload={'username': username},
                expires=cls.expires
            )

            return {'token': token}
        else:
            raise ApiException(USERNAME_OR_PASSWORD_ERROR)

    @classmethod
    def check_token(cls, token):
        # 测试环境下不校验
        if current_app.debug is True:
            return True

        try:
            jwt_util.decode(token)
        except Exception:
            raise ApiException(TOKEN_INVALID_ERROR)

    @classmethod
    def decode_token(cls, token):
        return jwt_util.decode(token)
