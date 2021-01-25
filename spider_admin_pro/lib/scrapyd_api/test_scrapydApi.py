# -*- coding: utf-8 -*-
from unittest import TestCase

from .scrapyd_client import ScrapydClient


class TestScrapydApi(TestCase):
    api = ScrapydClient()

    project = 'project'

    def test_daemon_status(self):
        print(self.api.daemon_status())

    def test_add_version(self):
        filename = '../scrapy_demo/demo.egg'
        with open(filename, 'rb') as egg:
            print(self.api.add_version(project=self.project, egg=egg))

    def test_schedule(self):
        print(self.api.schedule(project=self.project, spider='baidu-1', jobid='deebe7205e2311eb902eacde48001122'))

    def test_cancel(self):
        print(self.api.cancel(project=self.project, job=''))

    def test_delete_project(self):
        print(self.api.delete_project(project=self.project))

    def test_delete_version(self):
        print(self.api.delete_version(project=self.project, version='1610963908'))

    def test_list_jobs(self):
        print(self.api.list_jobs(project=self.project))

    def test_list_projects(self):
        print(self.api.list_projects())

    def test_list_spiders(self):
        print(self.api.list_spiders(project=self.project, _version='16109642778'))

    def test_list_versions(self):
        print(self.api.list_versions(project=self.project))

    def test_project_logs(self):
        print(self.api.project_logs(self.project))

    def test_logs(self):
        print(self.api.logs())

    def test_spider_logs(self):
        print(self.api.spider_logs(self.project, 'baidu'))

    def test_job_log(self):
        print(self.api.job_log(self.project, 'baidu', '53950cac597711eba57dacde48001122'))
