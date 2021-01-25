# -*- coding: utf-8 -*-
import traceback
from datetime import datetime

from flask import Flask, Blueprint, Request
from flask.json import JSONEncoder
from peewee import ModelSelect

from spider_admin_pro.exceptions.api_exception import ApiException
from spider_admin_pro.lib.flask_app.api_result import ApiResult
from collections import Iterable, Iterator


class CustomJSONEncoder(JSONEncoder):
    DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

    def default(self, o):
        if isinstance(o, ModelSelect):
            return list(o)

        if isinstance(o, datetime):
            return o.strftime(self.DATETIME_FORMAT)

        return super().default(o)


class CustomRequest(Request):
    @property
    def json(self):
        data = self.get_json()

        if not data:
            data = {}

        return data


class FlaskApp(Flask):
    json_encoder = CustomJSONEncoder

    request_class = CustomRequest

    def get(self, rule, **options):
        return self.route(rule, methods=['GET'], **options)

    def post(self, rule, **options):
        return self.route(rule, methods=['POST'], **options)

    def make_response(self, rv):

        if isinstance(rv, (Iterator, ModelSelect)):
            rv = list(rv)

        if isinstance(rv, (list, dict)) or rv is None:
            rv = ApiResult.success(rv)

        if isinstance(rv, ApiResult):
            rv = rv.to_dict()

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
