# -*- coding: utf-8 -*-
# ==============================================
# scrapyd 接口服务
# ==============================================

from flask import request

from spider_admin_pro.model import ScrapydServerModel
from spider_admin_pro.utils.flask_ext.flask_app import BlueprintAppApi
from spider_admin_pro.service.auth_service import AuthService
from spider_admin_pro.service.scrapyd_service import get_client, ScrapydService

scrapyd_api = BlueprintAppApi("scrapyd", __name__)


@scrapyd_api.before_request
def before_request():
    token = request.headers.get('Token')
    AuthService.check_token(token)


@scrapyd_api.post('/daemonStatus')
def daemon_status():
    scrapyd_server_id = request.json['scrapydServerId']
    scrapyd_server_row = ScrapydServerModel.get_by_id(scrapyd_server_id)

    client = get_client(scrapyd_server_row)

    return client.daemon_status()


@scrapyd_api.post('/addVersion')
def add_version():
    egg = request.files['egg']
    project = request.form['project']
    scrapyd_server_id = request.form['scrapydServerId']
    scrapyd_server_row = ScrapydServerModel.get_by_id(scrapyd_server_id)

    client = get_client(scrapyd_server_row)

    return client.add_version(project, egg)


@scrapyd_api.post('/listProjects')
def list_projects():
    scrapyd_server_id = request.json['scrapydServerId']
    scrapyd_server_row = ScrapydServerModel.get_by_id(scrapyd_server_id)

    client = get_client(scrapyd_server_row)

    return client.list_projects()


@scrapyd_api.post('/listVersions')
def list_versions():
    project = request.json['project']
    scrapyd_server_id = request.json['scrapydServerId']
    scrapyd_server_row = ScrapydServerModel.get_by_id(scrapyd_server_id)

    client = get_client(scrapyd_server_row)

    return client.list_versions_format(project=project)


@scrapyd_api.post('/listJobs')
def list_jobs():
    project = request.json['project']
    scrapyd_server_id = request.json['scrapydServerId']
    scrapyd_server_row = ScrapydServerModel.get_by_id(scrapyd_server_id)

    client = get_client(scrapyd_server_row)


    return client.list_jobs(project=project)


@scrapyd_api.post('/listJobsMerge')
def list_jobs_merge():
    project = request.json['project']
    status = request.json.get('status')

    scrapyd_server_id = request.json['scrapydServerId']
    scrapyd_server_row = ScrapydServerModel.get_by_id(scrapyd_server_id)

    client = get_client(scrapyd_server_row)

    return client.list_jobs_merge(project=project, status=status)


@scrapyd_api.post('/cancel')
def cancel():
    project = request.json['project']
    job = request.json['job']

    scrapyd_server_id = request.json['scrapydServerId']
    scrapyd_server_row = ScrapydServerModel.get_by_id(scrapyd_server_id)

    client = get_client(scrapyd_server_row)

    return client.cancel(project=project, job=job)


@scrapyd_api.post('/cancelAllJob')
def cancel_all_job():
    project = request.json['project']

    scrapyd_server_id = request.json['scrapydServerId']
    scrapyd_server_row = ScrapydServerModel.get_by_id(scrapyd_server_id)

    client = get_client(scrapyd_server_row)

    return client.cancel_all_job(project=project)


@scrapyd_api.post('/listSpiders')
def list_spiders():
    project = request.json['project']

    scrapyd_server_id = request.json['scrapydServerId']
    scrapyd_server_row = ScrapydServerModel.get_by_id(scrapyd_server_id)

    client = get_client(scrapyd_server_row)

    return client.list_spiders(project=project)


@scrapyd_api.post('/schedule')
def schedule():
    project = request.json['project']
    spider = request.json['spider']
    scrapyd_server_id = request.json['scrapydServerId']

    kwargs = {
        'project': project,
        'spider': spider,
        'scrapyd_server_id': scrapyd_server_id
    }

    # fix: 记录手动运行日志
    ScrapydService.run_spider(**kwargs)


@scrapyd_api.post('/deleteVersion')
def delete_version():
    project = request.json['project']
    version = request.json['version']
    scrapyd_server_id = request.json['scrapydServerId']
    scrapyd_server_row = ScrapydServerModel.get_by_id(scrapyd_server_id)

    client = get_client(scrapyd_server_row)

    return client.delete_version(project=project, version=version)


@scrapyd_api.post('/deleteProject')
def delete_project():
    project = request.json['project']
    scrapyd_server_id = request.json['scrapydServerId']
    scrapyd_server_row = ScrapydServerModel.get_by_id(scrapyd_server_id)

    client = get_client(scrapyd_server_row)

    return client.delete_project(project=project)


########################
#  日志
########################
@scrapyd_api.post('/logs')
def logs():
    scrapyd_server_id = request.json['scrapydServerId']
    scrapyd_server_row = ScrapydServerModel.get_by_id(scrapyd_server_id)

    client = get_client(scrapyd_server_row)

    return client.logs()


@scrapyd_api.post('/projectLogs')
def project_logs():
    project = request.json['project']
    scrapyd_server_id = request.json['scrapydServerId']
    scrapyd_server_row = ScrapydServerModel.get_by_id(scrapyd_server_id)

    client = get_client(scrapyd_server_row)

    return client.project_logs(project=project)


@scrapyd_api.post('/spiderLogs')
def spider_logs():
    project = request.json['project']
    spider = request.json['spider']
    scrapyd_server_id = request.json['scrapydServerId']
    scrapyd_server_row = ScrapydServerModel.get_by_id(scrapyd_server_id)

    client = get_client(scrapyd_server_row)

    return client.spider_logs(project=project, spider=spider)


@scrapyd_api.post('/jobLog')
def job_log():
    project = request.json['project']
    spider = request.json['spider']
    job = request.json['job']
    scrapyd_server_id = request.json['scrapydServerId']
    scrapyd_server_row = ScrapydServerModel.get_by_id(scrapyd_server_id)

    client = get_client(scrapyd_server_row)

    return client.job_log(project=project, spider=spider, job=job)
