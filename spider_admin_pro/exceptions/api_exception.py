# -*- coding: utf-8 -*-


class ApiException(Exception):
    def __init__(self, code_and_message_tuple):
        super().__init__()
        self.code, self.message = code_and_message_tuple
