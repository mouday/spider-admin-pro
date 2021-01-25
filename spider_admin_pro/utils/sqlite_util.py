# -*- coding: utf-8 -*-
import os
from urllib.parse import urlparse
import logging

logger = logging.getLogger(__name__)


def make_sqlite_dir(sqlite_url):
    """创建sqlite数据库的文件夹"""
    result = urlparse(sqlite_url)

    if result.scheme == 'sqlite':

        dirname = os.path.dirname(result.path[1:])

        if dirname and not os.path.exists(dirname):
            os.mkdir(dirname)
            logger.debug("create directory: %s", dirname)


if __name__ == '__main__':
    url = 'sqlite:///dbs/schedule_history.db?name=TOm'
    make_sqlite_dir(url)
