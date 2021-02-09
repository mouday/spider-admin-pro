# Spider Admin Pro

![PyPI](https://img.shields.io/pypi/v/spider-admin-pro.svg)
![PyPI - Downloads](https://img.shields.io/pypi/dm/spider-admin-pro)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/spider-admin-pro)
![PyPI - License](https://img.shields.io/pypi/l/spider-admin-pro)


Github: [https://github.com/mouday/spider-admin-pro](https://github.com/mouday/spider-admin-pro)

Gitee: [https://gitee.com/mouday/spider-admin-pro](https://gitee.com/mouday/spider-admin-pro)

Pypi: [https://pypi.org/project/spider-admin-pro](https://pypi.org/project/spider-admin-pro)

## 简介

Spider Admin Pro 是Spider Admin的升级版

1. 简化了一些功能；
2. 优化了前端界面，基于Vue的组件化开发；
3. 优化了后端接口，对后端项目进行了目录划分；
4. 整体代码利于升级维护。

![](https://github.com/mouday/spider-admin-pro/raw/master/doc/img/spider-admin-pro.png)

## 安装启动

方式一：
```bash
$ pip3 install spider-admin-pro

$ python3 -m spider_admin_pro.run
```

方式二：
```bash
$ git clone https://github.com/mouday/spider-admin-pro.git

$ python3 spider_admin_pro/run.py

或者

$ gunicorn spider_admin_pro.run:app
``` 

## 配置参数

在运行目录新建 `.env` 环境变量文件，默认参数如下

注意：为了与其他环境变量区分，使用`SPIDER_ADMIN_PRO_`作为变量前缀

```bash

# flask 服务配置
SPIDER_ADMIN_PRO_PORT = 5002
SPIDER_ADMIN_PRO_HOST = '127.0.0.1'

# 登录账号密码
SPIDER_ADMIN_PRO_USERNAME = admin
SPIDER_ADMIN_PRO_PASSWORD = "123456"
SPIDER_ADMIN_PRO_JWT_KEY = FU0qnuV4t8rr1pvg93NZL3DLn6sHrR1sCQqRzachbo0=

# token过期时间，单位天
SPIDER_ADMIN_PRO_EXPIRES = 7

# scrapyd地址, 结尾不要加斜杆
SPIDER_ADMIN_PRO_SCRAPYD_SERVER = 'http://127.0.0.1:6800'

# 调度器 调度历史存储设置
# mysql or sqlite and other, any database for peewee support
SPIDER_ADMIN_PRO_SCHEDULE_HISTORY_DATABASE_URL = 'sqlite:///dbs/schedule_history.db'

# 调度器 定时任务存储地址
SPIDER_ADMIN_PRO_JOB_STORES_DATABASE_URL = 'sqlite:///dbs/apscheduler.db'

```

使用`python3 -m` 运行，需要将变量加入到环境变量中，运行目录下新建文件`env.bash`

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


生成jwt key
```
$ python -c 'import base64;import os;print(base64.b64encode(os.urandom(32)).decode())'
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
## 项目截图

![](https://github.com/mouday/spider-admin-pro/raw/master/doc/img/dashboard.png)

![](https://github.com/mouday/spider-admin-pro/raw/master/doc/img/project.png)

![](https://github.com/mouday/spider-admin-pro/raw/master/doc/img/schedule.png)

![](https://github.com/mouday/spider-admin-pro/raw/master/doc/img/logs.png)


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

