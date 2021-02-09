# -*- coding: utf-8 -*-


from spider_admin_pro.config import SCRAPYD_SERVER
from spider_admin_pro.service.schedule_service import scheduler
from spider_admin_pro.service.scrapyd_service import client, ScrapydService
from spider_admin_pro.utils.system_info_util import SystemInfoUtil
from spider_admin_pro.version import VERSION


class SystemDataService(object):
    @classmethod
    def get_system_data(cls):
        try:
            res = client.daemon_status()
        except Exception:
            res = {}

        try:
            projects = len(client.list_projects())
        except Exception:
            projects = 0

        return [
            {
                'title': '项目数量',
                'count': projects,
                'route': {'name': 'project'}
            },
            {
                'title': '定时任务',
                'count': len(scheduler.get_jobs()),
                'route': {'name': 'schedule'}

            },
            {
                'title': '任务总数',
                'count': res.get('total', 0),
                'route': {'name': 'job'}
            },
            {
                'title': '等待任务',
                'count': res.get('pending', 0),
                'route': {'name': 'job', 'query': {'status': 'pending'}}
            },
            {
                'title': '运行任务',
                'count': res.get('running', 0),
                'route': {'name': 'job', 'query': {'status': 'running'}}
            },
            {
                'title': '完成任务',
                'count': res.get('finished', 0),
                'route': {'name': 'job', 'query': {'status': 'finished'}}
            }
        ]

    @classmethod
    def get_system_config(cls):

        return {
            'scrapyd': {
                'url': SCRAPYD_SERVER,
                'status': ScrapydService.get_status()
            },
            'spider_admin': {
                'version': VERSION
            }
        }

    @classmethod
    def get_system_info(cls):
        return {
            'virtual_memory': SystemInfoUtil.get_virtual_memory(),
            'disk_usage': SystemInfoUtil.get_disk_usage(),
            # 'net_io_counters': cls.get_net_io_counters(),
        }
