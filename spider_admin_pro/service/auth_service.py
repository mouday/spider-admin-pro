# -*- coding: utf-8 -*-
import os

from flask import current_app

from spider_admin_pro.config import (
    BASIC_AUTH_USERNAME,
    BASIC_AUTH_PASSWORD,
    BASIC_AUTH_EXPIRES,
    DATABASE_DIR)
from spider_admin_pro.exceptions.api_exception import ApiException
from spider_admin_pro.exceptions.constant import TOKEN_INVALID_ERROR, USERNAME_OR_PASSWORD_ERROR
from spider_admin_pro.utils import secret_util, cache_util
from spider_admin_pro.utils.jwt_util import JwtUtil


def get_jwt_key():
    default_jwt_key = secret_util.get_random_secret()

    return cache_util.get_cache('jwt-key.txt', default_jwt_key)


def get_password():
    return BASIC_AUTH_PASSWORD or cache_util.get_cache('default-password.txt', secret_util.get_random_password())


jwt_util = JwtUtil(key=get_jwt_key())


class AuthService(object):
    # 用户名、密码
    username = BASIC_AUTH_USERNAME
    password = get_password()

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
