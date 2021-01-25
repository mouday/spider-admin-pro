# -*- coding: utf-8 -*-

res = '''
Traceback (most recent call last):
  File "/Users/hina/.pyenv/versions/3.7.0/envs/py370/lib/python3.7/site-packages/scrapyd/webservice.py", line 21, in render
    return JsonResource.render(self, txrequest).encode('utf-8')
  File "/Users/hina/.pyenv/versions/3.7.0/envs/py370/lib/python3.7/site-packages/scrapyd/utils.py", line 20, in render
    r = resource.Resource.render(self, txrequest)
  File "/Users/hina/.pyenv/versions/3.7.0/envs/py370/lib/python3.7/site-packages/twisted/web/resource.py", line 250, in render
    return m(request)
  File "/Users/hina/.pyenv/versions/3.7.0/envs/py370/lib/python3.7/site-packages/scrapyd/webservice.py", line 49, in render_POST
    spiders = get_spider_list(project, version=version)
  File "/Users/hina/.pyenv/versions/3.7.0/envs/py370/lib/python3.7/site-packages/scrapyd/utils.py", line 137, in get_spider_list
    raise RuntimeError(msg.encode('unicode_escape') if six.PY2 else msg)
RuntimeError: Scrapy 1.6.0 - no active project

Unknown command: list

Use "scrapy" to see available commands


'''
