# -*- coding: utf-8 -*-
from spider_admin_pro.main import app

if __name__ == '__main__':
    print(app.url_map)
    app.run(debug=True, port=5001)
