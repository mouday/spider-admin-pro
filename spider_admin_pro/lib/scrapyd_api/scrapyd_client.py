# -*- coding: utf-8 -*-
import traceback
from datetime import datetime
from time import time
import re
from parsel import Selector
from operator import itemgetter

from .constants import FINISHED, PENDING, RUNNING, SCRAPYD_DATE_TIME_FORMAT, TARGET_DATE_TIME_FORMAT
from .exceptions import ScrapydException
from .scrapyd_api import ScrapydAPI


class ScrapydClient(ScrapydAPI):
    ERROR_LIST = [
        'RuntimeError',
        'FileNotFoundError'
    ]

    def after_request(self, response):
        print(response.text)

        if not response.ok:
            response.raise_for_status()

        # 处理json
        if response.headers['Content-Type'] == 'application/json':
            return super().after_request(response)

        # 处理文本内容
        else:
            response.encoding = response.apparent_encoding

            for error_name in self.ERROR_LIST:

                if error_name in response.text:
                    msg = self._match_error_message('RuntimeError', response.text)
                    raise ScrapydException(msg)

            return response.text

    def daemon_status(self):
        res = super().daemon_status()
        res['total'] = res['pending'] + res['running'] + res['finished']
        return res

    def list_format_versions(self, project):
        """
        约定：版本号version 都是10位整数的时间戳，即默认版本号

        :param project:
        :return:
        """
        versions = super().list_versions(project)['versions']

        return [
            {
                'version': version,
                'format_version': self._format_version(version)
            }
            for version in versions
        ]

    def add_version(self, project, egg, version=None):
        version = version or int(time())
        return super().add_version(project, version, egg)

    def list_spiders(self, project, _version=None):
        spiders = super().list_spiders(project, _version)['spiders']
        return [{'spider': spider} for spider in spiders]

    def list_projects(self):
        projects = super().list_projects()['projects']
        return [{'project': project} for project in projects]

    def list_versions(self, project):
        versions = super().list_versions(project)['versions']
        return [{'version': version} for version in versions]

    def delete_version(self, project, version):
        res = super().delete_version(project, version)
        return res

    def delete_project(self, project):
        res = super().delete_project(project)
        if 'NotADirectoryError' in res:
            raise ScrapydException('NotADirectoryError')
        elif 'FileNotFoundError' in res:
            raise ScrapydException('FileNotFoundError')
        else:
            return res

    #####################################################
    # 扩展的数据接口
    #####################################################

    def job_status(self, project, job):
        """查询任务状态"""
        res = self.list_jobs_merge(project=project)
        for item in res:
            if item['id'] == job:
                return item
        else:
            raise ScrapydException("没有找到该任务")

    def list_jobs_merge(self, project, status=None):
        """
        合并后的任务列表
        :param status: pending、running、finished
        :param project:
        :return: list
        """

        res = super().list_jobs(project=project)

        if 'KeyError' in res:
            raise Exception(f'project {project} not exists')

        print('res', res)

        lst = []

        if status:
            lst.extend(self._get_jobs_list(res, status))
        else:
            lst.extend(self._get_jobs_list(res, PENDING))

            running_list = self._get_jobs_list(res, RUNNING)
            running_list.sort(key=itemgetter('start_time'), reverse=True)
            lst.extend(running_list)

            finished_list = self._get_jobs_list(res, FINISHED)
            finished_list.sort(key=itemgetter('start_time'), reverse=True)
            lst.extend(finished_list)

        pending = len(res[PENDING])
        running = len(res[RUNNING])
        finished = len(res[FINISHED])
        total = pending + running + finished

        data = {
            'list': lst,
            'total': total,
            'pending': pending,
            'running': running,
            'finished': finished,
        }

        return data

    def cancel_all_project_job(self):
        """取消所有项目下的任务"""
        projects = super().list_projects()['projects']

        for project in projects:
            self.cancel_all_job(project=project)

    def cancel_all_job(self, project):
        """取消指定项目下的任务"""
        res = super().list_jobs(project=project)
        jobs = []

        jobs.extend(res['pending'])
        jobs.extend(res['running'])

        for job in jobs:
            super().cancel(project, job=job['id'])

    #####################################################
    # 扩展的日志接口
    #####################################################

    def logs(self):
        """获取日志-项目列表"""
        res = self.get(path='/logs')
        return self._parse_table(res)

    def project_logs(self, project):
        """获取日志-爬虫列表"""
        path = '/logs/{}'.format(project)

        res = self.get(path=path)
        return self._parse_table(res)

    def spider_logs(self, project, spider):
        """获取日志-任务列表"""
        path = '/logs/{}/{}'.format(project, spider)

        res = self.get(path=path)
        return self._parse_table(res)

    def job_log(self, project, spider, job):
        """获取job日志"""
        if not job.endswith('.log'):
            job = job + '.log'

        path = '/logs/{}/{}/{}'.format(project, spider, job)

        return self.get(path=path)

    #####################################################
    # 工具类方法
    #####################################################
    def _parse_table(self, text):
        """解析表格数据"""
        sel = Selector(text=text)
        rows = sel.css('table tbody tr')

        lst = []
        for row in rows:
            filename = row.css('td:nth-child(1) a::text').extract_first('')
            size = row.css('td:nth-child(2)::text').extract_first('')
            content_type = row.css('td:nth-child(3)::text').extract_first('')
            content_encoding = row.css('td:nth-child(4)::text').extract_first('')

            item = {
                'filename': filename.strip('/'),
                'size': size,
                'content_type': content_type,
                'content_encoding': content_encoding,
            }

            lst.append(item)

        return lst

    def _parse_date_time(self, date_time_str):
        if not date_time_str:
            return None

        return datetime.strptime(date_time_str, SCRAPYD_DATE_TIME_FORMAT)

    def _format_date_time(self, date_time):
        if not date_time:
            return ''

        return date_time.strftime(TARGET_DATE_TIME_FORMAT)

    def _convert_date_time(self, date_time):
        if not date_time:
            return ''

        return self._format_date_time(self._parse_date_time(date_time))

    def _get_duration(self, start_time, end_time):
        if not start_time or not end_time:
            return None

        return (end_time - start_time).seconds

    def _format_duration(self, seconds):
        """
        :param seconds: int
        :return: str
        """
        if not seconds:
            return ''

        hour, second = divmod(seconds, 60 * 60)
        minute, second = divmod(second, 60)

        if hour > 0:
            delta = "{}h: {}m: {}s".format(hour, minute, second)
        elif minute > 0:
            delta = "{}m: {}s".format(minute, second)
        else:
            delta = "{}s".format(second)

        return delta

    def _format_version(self, version):
        return self._format_date_time(datetime.fromtimestamp(int(version)))

    def _get_jobs_list(self, data, status):
        """
        获取单个状态下数据列表，统一格式
        :param data:
        :param status:
        :return:

        """

        lst = []

        if not status:
            return lst

        for row in data[status]:
            start_time = self._parse_date_time(row.get('start_time'))
            end_time = self._parse_date_time(row.get('end_time'))

            if start_time and end_time:
                duration = self._get_duration(start_time, end_time)
            else:
                duration = None

            item = {
                'status': status,
                'id': row['id'],
                'spider': row['spider'],
                'pid': row.get('pid', ''),
                'start_time': self._format_date_time(start_time),
                'end_time': self._format_date_time(end_time),
                'duration': duration,
                'duration_str': self._format_duration(duration),
            }

            lst.append(item)

        return lst

    def _match_error_message(self, keywords, text):

        match = re.search(f'{keywords}:.*', text)
        return match.group(0)
