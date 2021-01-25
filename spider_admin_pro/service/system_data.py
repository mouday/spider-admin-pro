# -*- coding: utf-8 -*-

from spider_admin_pro.api.schedule import scheduler
from spider_admin_pro.api.scrapyd import client
from spider_admin_pro.config import SCRAPYD_SERVER
import traceback


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
                'count': projects
            },
            {
                'title': '定时任务',
                'count': len(scheduler.get_jobs())
            },
            {
                'title': '任务总数',
                'count': res.get('total', 0)
            },
            {
                'title': '等待任务',
                'count': res.get('pending', 0)
            },
            {
                'title': '运行任务',
                'count': res.get('running', 0)
            },
            {
                'title': '完成任务',
                'count': res.get('finished', 0)
            }
        ]

    @classmethod
    def get_system_config(cls):

        try:
            res = client.daemon_status()
            print(res)
            status = True if res['status'] == 'ok' else False
        except Exception:
            status = False

        return {
            'scrapyd': {
                'url': SCRAPYD_SERVER,
                'status': status
            }

        }
