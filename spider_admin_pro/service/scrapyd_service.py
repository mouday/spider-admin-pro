# -*- coding: utf-8 -*-
import json

from spider_admin_pro.config import SCRAPYD_SERVER
from scrapyd_api import ScrapydClient

from spider_admin_pro.model.schedule_history_model import ScheduleHistoryModel

client = ScrapydClient(base_url=SCRAPYD_SERVER)


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

        schedule_job_id = kwargs.get('schedule_job_id')
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

        ScheduleHistoryModel.insert_row(
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
