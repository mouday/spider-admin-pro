# -*- coding: utf-8 -*-
import logging
import os

# 日志目录
LOG_DIR = 'logs'

# 日志时间显示
date_fmt = "%Y-%m-%d %H:%M:%S"
fmt = '%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s'

if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)


class Logger(object):
    logs = {}

    @classmethod
    def get_logger_filename(cls, logger_name):
        return os.path.join(LOG_DIR, '%s.log' % logger_name)

    @classmethod
    def create_logger(cls, logger_name):
        logger = logging.getLogger(logger_name)

        log_filename = cls.get_logger_filename(logger_name)

        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(fmt=fmt, datefmt=date_fmt)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        file_handler = logging.FileHandler(log_filename)
        file_handler.setFormatter(formatter)

        logger.addHandler(stream_handler)
        logger.addHandler(file_handler)

        return logger

    @classmethod
    def get_logger(cls, logger_name):
        if logger_name not in cls.logs:
            cls.logs[logger_name] = cls.create_logger(logger_name)

        return cls.logs[logger_name]
