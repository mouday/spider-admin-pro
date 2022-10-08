# Spider Admin Pro

![PyPI](https://img.shields.io/pypi/v/spider-admin-pro.svg)
![PyPI - Downloads](https://img.shields.io/pypi/dm/spider-admin-pro)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/spider-admin-pro)
![PyPI - License](https://img.shields.io/pypi/l/spider-admin-pro)


Github: [https://github.com/mouday/spider-admin-pro](https://github.com/mouday/spider-admin-pro)

Gitee: [https://gitee.com/mouday/spider-admin-pro](https://gitee.com/mouday/spider-admin-pro)

Pypi: [https://pypi.org/project/spider-admin-pro](https://pypi.org/project/spider-admin-pro)

- [目录](#spider-admin-pro)
  * [简介](#简介)
  * [安装启动](#安装启动)
  * [配置参数](#----)
  * [部署优化](#----)
  * [使用扩展](#----)
  * [技术栈](#----)
  * [项目结构](#----)
  * [经验总结](#----)
  * [TODO](#todo)
  * [项目赞助](#----)
  * [交流沟通](#----)
  * [项目截图](#----)

## 简介

Spider Admin Pro 是[Spider Admin](https://github.com/mouday/SpiderAdmin)的升级版

1. 简化了一些功能；
2. 优化了前端界面，基于Vue的组件化开发；
3. 优化了后端接口，对后端项目进行了目录划分；
4. 整体代码利于升级维护。
5. 目前仅对Python3进行了支持

![](https://github.com/mouday/spider-admin-pro/raw/master/doc/img/spider-admin-pro.png)

## 安装启动

本项目基于Python3.7.0 开发，所以推荐使用Python3.7.0及其以上版本

> 注意：python3.10版本，库collections 停用了，所以不能运行该项目

运行项目前，请先确保[scrapyd](https://pengshiyu.blog.csdn.net/article/details/79842514)服务已经启动

方式一：

```bash
$ pip3 install spider-admin-pro

$ python3 -m spider_admin_pro.run
```

方式二：(推荐，可能由于PIP新版本未及时发布，github代码会保持最新)
```bash
$ git clone https://github.com/mouday/spider-admin-pro.git

$ cd spider-admin-pro

# 安装依赖（建议：最好新建一个虚拟环境）
$ pip3 install -r requirements.txt 

# 以生产模式运行
$ python3 spider_admin_pro/run.py

# 以开发模式运行
$ python3 dev.py

```

> Windows系统环境变量中可能没有`python3`,可以试试`python dev.py`

## 配置参数

配置优先级：
```
yaml配置文件 >  env环境变量 > 默认配置 
```

1、默认配置

```bash

# flask 服务配置
PORT = 5002
HOST = '127.0.0.1'

# 登录账号密码
USERNAME = admin
PASSWORD = "123456"
JWT_KEY = FU0qnuV4t8rr1pvg93NZL3DLn6sHrR1sCQqRzachbo0=

# token过期时间，单位天
EXPIRES = 7

# scrapyd地址, 结尾不要加斜杆
SCRAPYD_SERVER = 'http://127.0.0.1:6800'

# 调度器 调度历史存储设置
# mysql or sqlite and other, any database for peewee support
SCHEDULE_HISTORY_DATABASE_URL = 'sqlite:///dbs/schedule_history.db'

# 调度器 定时任务存储地址
JOB_STORES_DATABASE_URL = 'sqlite:///dbs/apscheduler.db'

# 日志文件夹
LOG_DIR = 'logs'
```

2、env环境变量

在运行目录新建 `.env` 环境变量文件，默认参数如下

注意：为了与其他环境变量区分，使用`SPIDER_ADMIN_PRO_`作为变量前缀

如果使用`python3 -m` 运行，需要将变量加入到环境变量中，运行目录下新建文件`env.bash`

注意，此时等号后面不可以用空格

```bash
# flask 服务配置
export SPIDER_ADMIN_PRO_PORT=5002
export SPIDER_ADMIN_PRO_HOST='127.0.0.1'

# 登录账号密码
export SPIDER_ADMIN_PRO_USERNAME='admin'
export SPIDER_ADMIN_PRO_PASSWORD='123456'
export SPIDER_ADMIN_PRO_JWT_KEY='FU0qnuV4t8rr1pvg93NZL3DLn6sHrR1sCQqRzachbo0='

```

增加环境变量后运行
```bash
$ source env.bash

$ python3 -m spider_admin_pro.run

```

[注意]：

为了简化配置复杂度，方式2：env环境变量，计划将在下一版本移除

3、自定义配置

在运行目录下新建`config.yml` 文件，运行时会自动读取该配置文件

eg:

```yaml
# flask 服务配置
PORT: 5002
HOST: '127.0.0.1'

# 登录账号密码
USERNAME: admin
PASSWORD: "123456"
JWT_KEY: "FU0qnuV4t8rr1pvg93NZL3DLn6sHrR1sCQqRzachbo0="

# token过期时间，单位天
EXPIRES: 7

# scrapyd地址, 结尾不要加斜杆
SCRAPYD_SERVER: "http://127.0.0.1:6800"

# 日志文件夹
LOG_DIR: 'logs'
```

生成jwt key
```
$ python -c 'import base64;import os;print(base64.b64encode(os.urandom(32)).decode())'
```

## 部署优化

1、使用 Gunicorn管理应用

Gunicorn文档：[https://docs.gunicorn.org/](https://docs.gunicorn.org/)

```bash
# 启动服务
$ gunicorn --config gunicorn.conf.py spider_admin_pro.run:app
```

注意： 

如果使用了 `Gunicorn` 那么 配置文件中的 `PORT` 和 `HOST` 将会不生效

如果需要修改port 和host, 需要修改`gunicorn.conf.py` 文件中的 `bind`
 
一个配置示例：gunicorn.conf.py

```python
# -*- coding: utf-8 -*-

"""
$ gunicorn --config gunicorn.conf.py spider_admin_pro.run:app
"""

import multiprocessing
import os

from gevent import monkey

monkey.patch_all()

# 日志文件夹
LOG_DIR = 'logs'

if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)


def resolve_file(filename):
    return os.path.join(LOG_DIR, filename)


def get_workers():
    return multiprocessing.cpu_count() * 2 + 1


# daemon = True
daemon = False  # 使用supervisor不能是后台进程

# 进程名称
proc_name = "spider-admin-pro"

# 启动端口
bind = "127.0.0.1:5001"

# 日志文件
loglevel = 'debug'
pidfile = resolve_file("gunicorn.pid")
accesslog = resolve_file("access.log")
errorlog = resolve_file("error.log")

# 启动的进程数
# workers = get_workers()
workers = 2
worker_class = 'gevent'


# 启动时钩子
def on_starting(server):
    ip, port = server.address[0]
    print('server.address:', f'http://{ip}:{port}')

```

注意：

使用gunicorn部署，会启动多个worker, 这样apscheduler会启动多个，可能会出现重复运行的情况（暂时没出现）

这种情况下，调度器控制开关不要动，以免启动不了；如果出现了定时任务不执行，可尝试重启整个服务


2、使用supervisor管理进程

文档：[http://www.supervisord.org](http://www.supervisord.org)

spider-admin-pro.ini

```ini
[program: spider-admin-pro]
directory=/spider-admin-pro
command=/usr/local/python3/bin/gunicorn --config gunicorn.conf.py spider_admin_pro.run:app

stdout_logfile=logs/out.log
stderr_logfile=logs/err.log

stdout_logfile_maxbytes = 20MB
stdout_logfile_backups = 0
stderr_logfile_maxbytes=10MB
stderr_logfile_backups=0
```

3、使用Nginx转发请求

```bash
server {
    listen 80;

    server_name _;

    access_log  /var/log/nginx/access.log;
    error_log  /var/log/nginx/error.log;

    location / {
        proxy_pass         http://127.0.0.1:5001/;
        proxy_redirect     off;

        proxy_set_header   Host                 $host;
        proxy_set_header   X-Real-IP            $remote_addr;
        proxy_set_header   X-Forwarded-For      $proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Proto    $scheme;
    }
}

```

## 使用扩展

收集运行日志：[scrapy-util](https://github.com/mouday/scrapy-util) 可以帮助你收集到程序运行的统计数据


## 技术栈：
1、前端技术：

|  功能 | 第三方库及文档  |  
| - | -  | 
| 基本框架 | [vue](https://cn.vuejs.org/)  |
| 仪表盘图表 | [echarts](https://echarts.apache.org/)  |
| 网络请求 | [axios](https://www.npmjs.com/package/axios)  |
| 界面样式 | [Element-UI](https://element.eleme.cn/)  |


2、后端技术

| 功能 | 第三方库及文档 |
| - | -  |
| 接口服务 | [Flask](https://dormousehole.readthedocs.io/) |
| 任务调度 | [apscheduler](https://apscheduler.readthedocs.io/) |
| scrapyd接口 | [scrapyd-api](https://github.com/mouday/scrapyd-api) |
| 网络请求 | [session-request](https://github.com/mouday/session-request) |
| ORM | [peewee](http://docs.peewee-orm.com/) |
| jwt | [jwt](https://pyjwt.readthedocs.io/) |
| 系统信息 | [psutil](https://psutil.readthedocs.io/) |

## 项目结构

【公开仓库】基于Flask的后端项目spider-admin-pro: [https://github.com/mouday/spider-admin-pro](https://github.com/mouday/spider-admin-pro)

【私有仓库】基于Vue的前端项目spider-admin-pro-web: [https://github.com/mouday/spider-admin-pro-web](https://github.com/mouday/spider-admin-pro-web)


spider-admin-pro项目主要目录结构：

```bash
.
├── run.py        # 程序入口
├── api           # Controller层
├── service       # Sevice层
├── model         # Model层
├── exceptions    # 异常 
├── utils         # 工具类
└── web           # 静态web页

```

## 经验总结

Scrapyd 不能直接暴露在外网

1. 其他人通过deploy部署可以将代码部署到你的机器上，如果是root用户运行，还会在你机器上做其他的事情
2. 还有运行日志中会出现配置文件中的信息，存在信息泄露的危险


## TODO

~~1. 补全开发文档~~

~~2. 支持命令行安装可用~~

~~3. 优化代码布局，提取公共库~~

~~4. 日志自动刷新~~

~~5. scrapy项目数据收集~~

[ok]6. 定时任务spider列左对齐，支持本地排序

[x]7. 调度器控制移除停止开启开关，只保留暂停继续

[x]8. 添加任务，默认项目名，关闭弹框取消form校验结果

[x]9. 统计的日志量太大，增加一个一个定时清理的功能

[x]10. 定时任务备份，不小心把任务清空

[x]11. 希望能加入更好的定时方式,类似 scrapyd_web那种定时

[x]12. 简单的爬虫不用非要去打包，比如我自己上传一个py文件，可以定时任务，脚本的方式运行

## 交流沟通

关注本项目的小伙伴越来越多，为了更好地交流沟通，可以加入群聊

问题：邀请码 答案：SpiderAdmin

![](https://github.com/mouday/spider-admin-pro/raw/master/doc/img/qq.jpg)

## 项目赞助

| 日期 | 姓名 | 金额 | 
| - | - | - |
| 2022-04-16 | [@realhellosunsun](https://github.com/realhellosunsun) | ￥188.00
| 2022-08-30 | [@yangxiaozhe13](https://github.com/yangxiaozhe13) | ￥88.00
| 2022-09-01 | [@robot-2233](https://github.com/robot-2233) | ￥88.00

## 项目截图

![](https://github.com/mouday/spider-admin-pro/raw/master/doc/img/dashboard.png)

![](https://github.com/mouday/spider-admin-pro/raw/master/doc/img/project.png)

![](https://github.com/mouday/spider-admin-pro/raw/master/doc/img/schedule.png)

![](https://github.com/mouday/spider-admin-pro/raw/master/doc/img/logs.png)


## 二次开发

```bash
git clone https://github.com/mouday/spider-admin-pro.git

cd spider-admin-pro

python3 dev.py
```

## 安装升级
```
pip3 install -U spider-admin-pro -i https://pypi.org/simple
```

## 更新日志

1. 2021-09-03 [bugfix]修复【任务列表】运行中项目无法取消的bug

2. 2022-04-01 [bugfix] 当修改scrapyd的端口号后，在配置文件中指定scrapyd为修改后的端口号。配置文件不生效

感谢：@洒脱的狂者 发现的问题及解决办法

2. 2022-05-27 [update] requirements.txt 文件中增加 flask_cors 依赖

## Stargazers over time

[![Stargazers over time](https://starchart.cc/mouday/spider-admin-pro.svg)](https://starchart.cc/mouday/spider-admin-pro)


社区其他优秀工具推荐

- https://github.com/DormyMo/SpiderKeeper
- https://github.com/my8100/scrapydweb
- https://github.com/ouqiang/gocron 使用Go语言开发的轻量级定时任务集中调度和管理系统, 用于替代Linux-crontab
