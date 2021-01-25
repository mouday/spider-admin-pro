# -*- coding: utf-8 -*-
import json

from spider_admin_pro.config import SCRAPYD_SERVER
from scrapyd_api import ScrapydClient
from spider_admin_pro.model.history import HistoryModel

client = ScrapydClient(base_url=SCRAPYD_SERVER)


class ScrapydService(object):

    @classmethod
    def run_spider(cls, **kwargs):
        """
        运行爬虫函数
        :param kwargs:
            project 项目名 str
            spider  爬虫名 str
            options 其他参数 dict
        :return:
        """
        project = kwargs['project']
        schedule_job_id = kwargs['schedule_job_id']
        spider = kwargs['spider']
        options = kwargs.get('options')

        # 默认值处理
        if options:
            opts = json.loads(options)
        else:
            opts = {}

        try:
            res = client.schedule(project=project, spider=spider, **opts)
            spider_job_id = res['jobid']
            message = ''

        except Exception as e:
            message = str(e)
            spider_job_id = ''

        HistoryModel.insert_row(
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
            res = client.daemon_status()
            status = True if res['status'] == 'ok' else False
        except Exception:
            status = False

        return status


if __name__ == '__main__':
    ScrapydService.run_spider(project='project', spider='baidu', schedule_job_id="xx")
