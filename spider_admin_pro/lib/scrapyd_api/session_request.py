# -*- coding: utf-8 -*-
from requests import Session


class SessionRequest(object):

    def __init__(self, base_url='', **kwargs):
        """

        :param base_url: 用于和参数path进行拼接
        :param kwargs: requests.request 方法支持的所有参数
        """
        self.base_url = base_url
        self.kwargs = kwargs
        self.client = Session()

    def before_request(self, options):
        """请求前 参数处理器"""
        if 'path' in options:
            url = self.base_url + options.pop('path')
            options.setdefault('url', url)

        return options

    def after_request(self, response):
        """请求后 响应处理器"""
        return response

    def request(self, **kwargs):
        """请求处理器"""
        options = self.before_request({**self.kwargs, **kwargs})

        response = self.client.request(**options)

        return self.after_request(response)

    def get(self, **kwargs):
        return self.request(method='GET', **kwargs)

    def post(self, **kwargs):
        return self.request(method='POST', **kwargs)

    def delete(self, **kwargs):
        return self.request(method='DELETE', **kwargs)

    def options(self, **kwargs):
        return self.request(method='OPTIONS', **kwargs)

    def head(self, **kwargs):
        return self.request(method='HEAD', **kwargs)

    def put(self, **kwargs):
        return self.request(method='PUT', **kwargs)

    def patch(self, **kwargs):
        return self.request(method='PATCH', **kwargs)
