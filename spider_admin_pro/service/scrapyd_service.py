# -*- coding: utf-8 -*-
import json

from requests.auth import HTTPBasicAuth
from scrapyd_api import ScrapydClient

from spider_admin_pro.enums.schedule_type_enum import ScheduleTypeEnum
from spider_admin_pro.model.schedule_history_model import ScheduleHistoryModel
from spider_admin_pro.service import scrapyd_server_service


def get_client(scrapyd_server_row):
    """
    获取scrapyd 客户端的工厂方法
    @since 2.0.8
    :return:
    """

    params = {
        'base_url': scrapyd_server_row.server_url.rstrip('/')
    }

    if scrapyd_server_row.username and scrapyd_server_row.password:
        params.update({
            'auth': HTTPBasicAuth(scrapyd_server_row.username, scrapyd_server_row.password)
        })

    return ScrapydClient(**params)


class ScrapydService(object):

    @classmethod
    def run_spider(cls, **kwargs):
        """
        运行爬虫函数
        :param kwargs:
            必传：
            project 项目名 str
            spider  爬虫名 str

            可选：
            schedule_job_id 调度任务id，
                如果为空字符串：是手动调度，
                否则是自动调度

            options 其他参数 dict
        :return:
        """
        project = kwargs['project']
        spider = kwargs['spider']
        scrapyd_server_id = kwargs['scrapyd_server_id']
        schedule_type = kwargs.get('schedule_type') or ScheduleTypeEnum.ONLY_ONE_SERVER

        schedule_job_id = kwargs.get('schedule_job_id')
        options = kwargs.get('options')

        # 默认值处理
        if options:
            opts = json.loads(options)
        else:
            opts = {}

        try:
            if schedule_type == ScheduleTypeEnum.RANDOM_SERVER:
                # 随机轮询
                scrapyd_server_row = scrapyd_server_service.get_available_scrapyd_server()
            else:
                # 指定服务器
                scrapyd_server_row = scrapyd_server_service.get_available_scrapyd_server_by_id(
                    scrapyd_server_id=scrapyd_server_id
                )

            if not scrapyd_server_row:
                raise Exception("没有可用的scrapyd")

            scrapyd_server_id = scrapyd_server_row.id

            client = get_client(scrapyd_server_row)

            res = client.schedule(project=project, spider=spider, **opts)

            spider_job_id = res['jobid']
            message = ''

        except Exception as e:
            message = str(e)
            spider_job_id = ''

        ScheduleHistoryModel.insert_row(
            scrapyd_server_id=scrapyd_server_id,
            project=project,
            spider=spider,
            schedule_job_id=schedule_job_id,
            spider_job_id=spider_job_id,
            options=options,
            message=message
        )

    @classmethod
    def get_status(cls):
        try:
            client = get_client(None)

            res = client.daemon_status()
            status = True if res['status'] == 'ok' else False
        except Exception:
            status = False

        return status


if __name__ == '__main__':
    ScrapydService.run_spider(project='project', spider='baidu', schedule_job_id="xx")
