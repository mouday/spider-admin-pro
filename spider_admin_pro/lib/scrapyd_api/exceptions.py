# -*- coding: utf-8 -*-


class ScrapydException(Exception):
    def __init__(self, message):
        super().__init__(message)
