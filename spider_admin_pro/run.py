# -*- coding: utf-8 -*-
from spider_admin_pro.config import FLASK_PORT, FLASK_HOST
from spider_admin_pro.main import app

if __name__ == '__main__':
    app.run(port=FLASK_PORT, host=FLASK_HOST)
