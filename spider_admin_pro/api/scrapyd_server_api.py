# -*- coding: utf-8 -*-
"""
@File    : scrapyd_server_api.py
@Date    : 2024-07-13
"""

from flask import request

from spider_admin_pro.model.scrapyd_server_model import ScrapydServerModel
from spider_admin_pro.service.auth_service import AuthService
from spider_admin_pro.utils.flask_ext.flask_app import BlueprintAppApi

scrapyd_server_api = BlueprintAppApi("scrapydServer", __name__)


@scrapyd_server_api.before_request
def before_request():
    token = request.headers.get('Token')
    AuthService.check_token(token)


@scrapyd_server_api.post('/addScrapydServer')
def add_scrapyd_server():
    server_url = request.json['server_url']
    server_name = request.json['server_name']
    username = request.json['username']
    password = request.json['password']
    status = request.json['status']

    ScrapydServerModel.create(
        server_url=server_url,
        server_name=server_name,
        username=username,
        password=password,
        status=status,
    )


@scrapyd_server_api.post('/updateScrapydServer')
def update_scrapyd_server():
    scrapyd_server_id = request.json['scrapyd_server_id']
    server_url = request.json['server_url']
    server_name = request.json['server_name']
    username = request.json['username']
    password = request.json['password']
    status = request.json['status']

    ScrapydServerModel.update(
        server_url=server_url,
        server_name=server_name,
        username=username,
        password=password,
        status=status,
    ).where(
        ScrapydServerModel.id == scrapyd_server_id
    ).execute()


@scrapyd_server_api.post('/updateScrapydServerStatus')
def update_scrapyd_server_status():
    scrapyd_server_id = request.json['scrapyd_server_id']
    status = request.json['status']

    ScrapydServerModel.update(
        status=status,
    ).where(
        ScrapydServerModel.id == scrapyd_server_id
    ).execute()


@scrapyd_server_api.post('/deleteScrapydServer')
def delete_scrapyd_server():
    scrapyd_server_id = request.json['scrapyd_server_id']

    ScrapydServerModel.delete().where(
        ScrapydServerModel.id == scrapyd_server_id
    ).execute()


@scrapyd_server_api.post('/getScrapydServer')
def get_scrapyd_server():
    scrapyd_server_id = request.json['scrapyd_server_id']

    return ScrapydServerModel.get_by_id(scrapyd_server_id)


@scrapyd_server_api.post('/getScrapydServerPage')
def get_scrapyd_server_page():
    lst = ScrapydServerModel.select()
    total = ScrapydServerModel.select().count()

    return {
        'list': lst,
        'total': total
    }
