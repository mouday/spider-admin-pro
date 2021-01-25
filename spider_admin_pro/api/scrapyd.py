# -*- coding: utf-8 -*-
# ==============================================
# scrapyd 接口服务
# ==============================================

from flask import request

from spider_admin_pro.lib.flask_app.flask_app import BlueprintAppApi
from spider_admin_pro.service.auth import AuthService
from spider_admin_pro.service.scrapyd_service import client

scrapyd_api = BlueprintAppApi("scrapyd", __name__)


@scrapyd_api.before_request
def before_request():
    token = request.headers.get('Token')
    AuthService.check_token(token)


@scrapyd_api.post('/daemonStatus')
def daemon_status():
    return client.daemon_status()


@scrapyd_api.post('/addVersion')
def add_version():
    project = request.form['project']
    egg = request.files['egg']

    return client.add_version(project, egg)


@scrapyd_api.post('/listProjects')
def list_projects():
    return client.list_projects()


@scrapyd_api.post('/listVersions')
def list_versions():
    project = request.json['project']

    return client.list_format_versions(project=project)


@scrapyd_api.post('/listJobs')
def list_jobs():
    project = request.json['project']

    return client.list_jobs(project=project)


@scrapyd_api.post('/listJobsMerge')
def list_jobs_merge():
    project = request.json['project']
    status = request.json.get('status')

    return client.list_jobs_merge(project=project, status=status)


@scrapyd_api.post('/cancel')
def cancel():
    project = request.json['project']
    job = request.json['job']

    return client.cancel(project=project, job=job)


@scrapyd_api.post('/cancelAllJob')
def cancel_all_job():
    project = request.json['project']

    return client.cancel_all_job(project=project)


@scrapyd_api.post('/listSpiders')
def list_spiders():
    project = request.json['project']

    return client.list_spiders(project=project)


@scrapyd_api.post('/schedule')
def schedule():
    project = request.json['project']
    spider = request.json['spider']

    return client.schedule(project=project, spider=spider)


@scrapyd_api.post('/deleteVersion')
def delete_version():
    project = request.json['project']
    version = request.json['version']

    return client.delete_version(project=project, version=version)


@scrapyd_api.post('/deleteProject')
def delete_project():
    project = request.json['project']

    return client.delete_project(project=project)


########################
#  日志
########################
@scrapyd_api.post('/logs')
def logs():
    return client.logs()


@scrapyd_api.post('/projectLogs')
def project_logs():
    project = request.json['project']

    return client.project_logs(project=project)


@scrapyd_api.post('/spiderLogs')
def spider_logs():
    project = request.json['project']
    spider = request.json['spider']

    return client.spider_logs(project=project, spider=spider)


@scrapyd_api.post('/jobLog')
def job_log():
    project = request.json['project']
    spider = request.json['spider']
    job = request.json['job']

    return client.job_log(project=project, spider=spider, job=job)
