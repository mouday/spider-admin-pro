# Spider Admin Pro

## 简介

Github: [https://github.com/mouday/spider-admin-pro](https://github.com/mouday/spider-admin-pro)

Gitee: [https://gitee.com/mouday/spider-admin-pro](https://gitee.com/mouday/spider-admin-pro)

Pypi: [https://pypi.org/project/spider-admin-pro](https://pypi.org/project/spider-admin-pro)


## 技术栈：
1、前端技术：

|  功能 | 第三方库及文档  |  
| - | -  | 
| 仪表盘图表 | [echarts](https://echarts.apache.org/)  |


2、后端技术
| 功能 | 第三方库及文档 |
| - | -  | 
| 接口服务 | [Flask](https://dormousehole.readthedocs.io/) |
| 任务调度 | [apscheduler](https://apscheduler.readthedocs.io/) |
| scrapyd接口 | [scrapyd-api](https://github.com/mouday/scrapyd-api) |
| ORM: | [peewee](http://docs.peewee-orm.com/) |
| jwt: | [jwt](https://pyjwt.readthedocs.io/) |

## 项目结构

【公开仓库】基于Flask的后端项目spider-admin-pro: [https://github.com/mouday/spider-admin-pro-web/](https://github.com/mouday/spider-admin-pro)

【私有仓库】基于Vue的前端项目spider-admin-pro-web: [https://github.com/mouday/spider-admin-pro-web/](https://github.com/mouday/spider-admin-pro-web/)


spider-admin-pro项目结构：

```bash
.
├── __init__.py
├── run.py
├── main.py
├── config.py
├── version.py
├── flask_app.py
├── logger.py
├── api_result.py
├── api
│   ├── __init__.py
│   ├── auth_api.py
│   ├── schedule_api.py
│   ├── scrapyd_api.py
│   └── system_info_api.py
├── service
│   ├── __init__.py
│   ├── auth_service.py
│   ├── schedule_service.py
│   ├── scrapyd_service.py
│   └── system_data_service.py
├── model
│   ├── __init__.py
│   ├── base.py
│   └── history.py
├── exceptions
│   ├── __init__.py
│   ├── api_exception.py
│   └── constant.py
├── utils
│   ├── __init__.py
│   ├── jwt_util.py
│   ├── scheduler_util.py
│   ├── sqlite_util.py
│   └── system_info_util.py
└── web
    ├── __init__.py
    ├── main.py
    └── public
        ├── index.html
        └── static
```
## 项目截图

![](doc/img/dashboard.png)

![](doc/img/project.png)

![](doc/img/schedule.png)

![](doc/img/logs.png)



## TODO

1. 补全开发文档
2. 支持命令行安装可用
3. 优化代码布局，提取公共库
