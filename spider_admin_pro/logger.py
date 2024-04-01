# -*- coding: utf-8 -*-
import logging
from logging.handlers import RotatingFileHandler

from spider_admin_pro.config import resolve_log_file

logger = logging.getLogger(__name__)
file_handler = RotatingFileHandler(
    filename=resolve_log_file('spider-admin-pro.log'),
    maxBytes=1024 * 1024 * 1,  # 1MB
    backupCount=1,
    encoding='utf-8'
)

logger.addHandler(logging.StreamHandler())

logger.addHandler(file_handler)

logger.setLevel(logging.DEBUG)
