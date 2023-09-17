# -*- coding: utf-8 -*-
import traceback
from typing import Iterator

import six
from flask import Flask, Blueprint, Response
from peewee import ModelSelect, Model

from spider_admin_pro.api_result import ApiResult
from spider_admin_pro.exceptions.api_exception import ApiException
from spider_admin_pro.utils.flask_ext.request import FlaskRequest


class FlaskApp(Flask):
    """
    扩展Flask
    """
    request_class = FlaskRequest

    # 需要转为json的类型
    json_data_class = (
        ModelSelect,
        Model,
        Iterator,
        list,
        dict,
        six.integer_types,
        six.text_type
    )

    def get(self, rule, **options):
        return self.route(rule, methods=['GET'], **options)

    def post(self, rule, **options):
        return self.route(rule, methods=['POST'], **options)

    def make_response(self, rv):

        if isinstance(rv, self.json_data_class) or rv is None:
            rv = ApiResult.success(rv)

        if isinstance(rv, ApiResult):
            return Response(rv.to_json(), content_type='application/json;charset=utf-8')

        return super().make_response(rv)


class BlueprintApp(Blueprint):
    def get(self, rule, **options):
        return self.route(rule, methods=['GET'], **options)

    def post(self, rule, **options):
        return self.route(rule, methods=['POST'], **options)


class BlueprintAppApi(BlueprintApp):
    """API统一处理"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register_error_handler(Exception, self._error_handler)

    def _error_handler(self, e):
        print('@BlueprintAppApi.errorhandler')
        traceback.print_exc()

        if isinstance(e, ApiException):
            result = ApiResult.failure(msg=e.message, code=e.code)
        else:
            result = ApiResult.failure(msg=str(e))

        return result
