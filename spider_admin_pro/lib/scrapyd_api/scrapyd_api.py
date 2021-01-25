from __future__ import unicode_literals

from spider_admin_pro.lib.scrapyd_api.exceptions import ScrapydException
from spider_admin_pro.lib.scrapyd_api.session_request import SessionRequest


class ScrapydAPI(SessionRequest):
    """
    文档
    https://scrapyd.readthedocs.io/en/stable/api.html
    """

    def __init__(self, base_url='http://localhost:6800', **kwargs):
        super().__init__(base_url, **kwargs)

    def after_request(self, response):
        """请求后 响应处理器"""
        res = response.json()

        if res['status'] == 'ok':
            return res
        else:
            raise ScrapydException(res['message'])

    def add_version(self, project, version, egg):
        """
        Add a version to a project, creating the project if it doesn’t exist.

        :param project: the project name
        :param version: the spider name
        :param egg: a Python egg containing the project’s code

        """

        options = {
            'path': '/addversion.json',
            'data': {
                'project': project,
                'version': version
            },
            'files': {'egg': egg}
        }

        return self.post(**options)

    def cancel(self, project, job):
        """
         Cancel a spider run (aka. job).
         If the job is pending, it will be removed.
         If the job is running, it will be terminated.

         :param project: the project name
         :param job: the job id
        """
        options = {
            'path': '/cancel.json',
            'data': {
                'project': project,
                'job': job
            }
        }
        self.post(**options)

    def delete_project(self, project):
        """
        Deletes all versions of a project. First class, maps to Scrapyd's
        delete project endpoint.
        """
        options = {
            'path': '/delproject.json',
            'data': {
                'project': project
            },

        }
        return self.post(**options)

    def delete_version(self, project, version):
        """
        Deletes a specific version of a project. First class, maps to
        Scrapyd's delete version endpoint.
        """
        options = {
            'path': '/delversion.json',
            'data': {
                'project': project,
                'version': version
            },
        }
        return self.post(**options)

    def list_jobs(self, project):
        """
        Get the list of pending, running and finished jobs of some project.

        :param project:  the project name

        {
            "status": "ok",
            "pending": [{"id": "78391cc0fcaf11e1b0090800272a6d06", "spider": "spider1"}],
            "running": [{"id": "422e608f9f28cef127b3d5ef93fe9399", "spider": "spider2",
                        "start_time": "2012-09-12 10:14:03.594664"}],
            "finished": [{"id": "2f16646cfcaf11e1b0090800272a6d06", "spider": "spider3",
                        "start_time": "2012-09-12 10:14:03.594664",
                        "end_time": "2012-09-12 10:24:03.594664"}]
        }
        """
        options = {
            'path': '/listjobs.json',
            'params': {
                'project': project
            }
        }

        return self.get(**options)

    def list_projects(self):
        """
        Get the list of projects uploaded to this Scrapy server.

        {"status": "ok", "projects": ["myproject", "otherproject"]}
        """

        options = {
            'path': '/listprojects.json'
        }

        return self.get(**options)

    def list_spiders(self, project, _version=None):
        """
        Get the list of spiders available in the last (unless overridden) version of some project.

        :param project: the project name
        :param _version: the version of the project to examine

        """
        options = {
            'path': '/listspiders.json',
            'params': {
                'project': project,
                '_version': _version
            }
        }

        return self.get(**options)

    def list_versions(self, project):
        """
        Get the list of versions available for some project.
        The versions are returned in order, the last one is the currently used version.

        :param project:  the project name

        """
        options = {
            'path': '/listversions.json',
            'params': {
                'project': project
            }
        }

        return self.get(**options)

    def schedule(self, project, spider, setting=None, jobid=None, _version=None, **kwargs):
        """
        Schedule a spider run (also known as a job), returning the job id.

        :param project: the project name
        :param spider: the spider name
        :param setting: a Scrapy setting to use when running the spider
            eg: setting=DOWNLOAD_DELAY=2
        :param jobid:  a job id used to identify the job, overrides the default generated UUID
        :param _version: the version of the project to use
        :param kwargs: any other parameter is passed as spider argument

        """

        params = {
            'path': '/schedule.json',
            'data': {
                'project': project,
                'spider': spider,
                'setting': setting,
                'jobid': jobid,
                '_version': _version,
                **kwargs
            }

        }
        return self.post(**params)

    def daemon_status(self):
        """
        Displays the load status of a service.
        :rtype: dict
        """
        params = {
            'path': '/daemonstatus.json'
        }
        return self.get(**params)


if __name__ == '__main__':
    api = ScrapydAPI()
    print(api.daemon_status())
    print(api.add_version(1, 2, 3))
