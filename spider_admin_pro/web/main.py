# -*- coding: utf-8 -*-

from spider_admin_pro.utils.flask_ext.flask_app import BlueprintAppApi

from flask import send_file

web = BlueprintAppApi(
    name="web",
    import_name=__name__,
    root_path="web",
    static_folder='public/static',
    static_url_path="static",
)


@web.get("/")
def index():
    # 转发
    return send_file('web/public/index.html')
