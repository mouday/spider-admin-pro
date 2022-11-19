# -*- coding: utf-8 -*-
from flask import Request


class FlaskRequest(Request):
    @property
    def json(self):
        """
        强制返回json
        :return:
        """
        return self.get_json(force=True, silent=True) or {}
