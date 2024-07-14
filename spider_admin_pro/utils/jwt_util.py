# -*- coding: utf-8 -*-
import time
from datetime import datetime, timedelta

import jwt


class JwtUtil(object):
    def __init__(self, key):
        self.key = key

    def encode(self, payload, expires=7):
        """
        获取token
        :param payload: dict
        :param expires: 过期时间：天
        :return: byte
        """

        # 使用utc时间
        payload['exp'] = datetime.utcnow() + timedelta(days=expires)

        # 返回 str 部分Python版本会报错
        return jwt.encode(payload=payload, key=self.key, algorithm='HS256')

    def decode(self, token):
        """
        验证并解析token
        :param token: str
        :return:  dict
        """
        return jwt.decode(jwt=token.encode(), key=self.key, algorithms=['HS256'])


if __name__ == '__main__':
    k = 'ddd'
    data = {'name': 'Tom'}
    w = JwtUtil(k)

    tk = w.encode(data, expires=0)
    print(tk)
    print(w.decode(tk))

    time.sleep(1)
    j = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJuYW1lIjoiVG9tIiwiZXhwIjoxNjExMTUyODcxfQ.-hGPmGqyyWIBBcQSYqqpVaDRc7pywTw5KYhmT69Zp6c'

    print(w.decode(tk))
