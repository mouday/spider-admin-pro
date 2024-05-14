# Spider Admin Pro

[![PyPI](https://img.shields.io/pypi/v/spider-admin-pro.svg)](https://pypi.org/project/spider-admin-pro)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/spider-admin-pro)](https://pypi.org/project/spider-admin-pro)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/spider-admin-pro)](https://pypi.org/project/spider-admin-pro)
[![Docker Image Version (latest semver)](https://img.shields.io/docker/v/mouday/spider-admin-pro?label=docker%20version&sort=semver)](https://hub.docker.com/r/mouday/spider-admin-pro)
[![Docker Pulls](https://img.shields.io/docker/pulls/mouday/spider-admin-pro)](https://app.travis-ci.com/mouday/spider-admin-pro)
[![Build Status](https://app.travis-ci.com/mouday/spider-admin-pro.svg?branch=master)](https://app.travis-ci.com/mouday/spider-admin-pro)
[![PyPI - License](https://img.shields.io/pypi/l/spider-admin-pro)](https://github.com/mouday/spider-admin-pro/blob/master/LICENSE)

![](https://github.com/mouday/spider-admin-pro/raw/master/doc/img/logo.png)

## 简介

Spider Admin Pro 是[Spider Admin](https://github.com/mouday/SpiderAdmin)的升级版，一个可视化的Scrapy爬虫管理平台，依赖于Scrapyd

- Github: [https://github.com/mouday/spider-admin-pro](https://github.com/mouday/spider-admin-pro)
- Gitee: [https://gitee.com/mouday/spider-admin-pro](https://gitee.com/mouday/spider-admin-pro)

- Pypi: [https://pypi.org/project/spider-admin-pro](https://pypi.org/project/spider-admin-pro)
- Docker: [https://hub.docker.com/r/mouday/spider-admin-pro](https://hub.docker.com/r/mouday/spider-admin-pro)
- releases: [https://github.com/mouday/spider-admin-pro/releases](https://github.com/mouday/spider-admin-pro/releases)

![](https://github.com/mouday/spider-admin-pro/raw/master/doc/img/spider-admin-pro.png)

## 安装启动

本项目基于Python3.7.0 开发，所以推荐使用Python3.7.0及其以上版本

运行项目前，请先确保[scrapyd](https://pengshiyu.blog.csdn.net/article/details/79842514)服务已经启动

方式一：

```bash
$ python3 --version
Python 3.7.0

# 创建名为 venv 的虚拟环境
$ python3 -m venv venv

# 激活虚拟环境
$ source venv/bin/activate

# 安装spider-admin-pro
$ pip3 install spider-admin-pro

# 可选
$ pip3 install -U spider-admin-pro -i https://pypi.org/simple

# Linux macOS 运行启动
$ gunicorn 'spider_admin_pro:app'

# windows 环境使用waitress 替换 gunicorn
$ pip install waitress

$ waitress-serve --listen=127.0.0.1:8000 'spider_admin_pro:app'
```

方式二：

```bash
$ git clone https://github.com/mouday/spider-admin-pro.git

$ cd spider-admin-pro

# 安装依赖（建议：最好新建一个虚拟环境）
$ pip3 install -r requirements.txt 

# Linux/macOS 以开发模式运行
$ make dev

# windows 以开发模式运行
$ python3 dev.py

# 以生产模式运行
$ make pro
```

安装 scrapy 全家桶`[可选]`

```bash
pip install scrapy scrapyd scrapyd-client
```

方式三：

```bash
vim config.yaml # 配置文件文件内容见⬇️：配置参数
docker run -e TZ=Asia/Shanghai -p 8000:8000 -v ./config.yml:/app/config.yml mouday/spider-admin-pro
```

## 配置参数

> - v2.0版本移除了`.env`环境变量配置方式，仅支持yaml格式配置
> - v2.0版本移除了`PORT`和`HOST`配置项，推荐统一采用gunicorn 管理

[Spider Admin Pro V1版本文档看这里](README-v1.md)

自定义配置

在运行目录下新建`config.yml` 文件，也就是执行启动命令的目录，运行时会自动读取该配置文件

例如
```bash
$ ls
config.yml

$ gunicorn 'spider_admin_pro:app'
```
> 强烈建议：修改密码和秘钥项

eg:

```yaml
# 登录账号密码
USERNAME: admin
PASSWORD: "123456"

# scrapyd地址, 结尾不要加斜杆
SCRAPYD_SERVER: "http://127.0.0.1:6800"

# 【可选】支持 basic auth @since 2.0.8 
SCRAPYD_USERNAME: ''
SCRAPYD_PASSWORD: ''
```

## 使用扩展

收集运行日志：[scrapy-util](https://github.com/mouday/scrapy-util) 可以帮助你收集到程序运行的统计数据

## 技术栈：

1、前端技术：

|  功能 | 第三方库及文档  |  
| - | -  | 
| 基本框架 | [vue2.js](https://cn.vuejs.org/)  |
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

> 备注：前端Vue项目，可入QQ群发送github用户名获取权限

获取前端源码的几个方式：

- 方式一：提供github的用户名

- 方式二：先赞助项目￥10，再提供github的用户名

- 方式三：关注微信公众号：

<img src="https://gitee.com/mouday/domain-admin/raw/master/image/coding-big-tree.jpg" width="300">

回复：`spider-admin-web`，获取完整的前端代码

回复：`spider-admin`，可加入Python技术交流群，和更多开发者学习交流遇到的问题

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

[x]13. 爬虫能配置带参数运行

## 交流沟通

关注本项目的小伙伴越来越多，为了更好地交流沟通，可以加入群聊

- 一群: 1074075691（已满）
- 二群: 864983297

问题：邀请码 答案：SpiderAdmin

<img src="https://github.com/mouday/spider-admin-pro/raw/master/doc/img/qq-2.jpg" width="300"/>

## 联系作者

微信扫码二维码

<img src="https://raw.githubusercontent.com/mouday/domain-admin/master/image/coding-big-tree.jpg" width="300">

扫描二维码后，回复：Python，即可进入Python技术交流群，和技术大佬们学习交流

## 项目赞助

| 日期 | 姓名 | 金额 | 
| - | - | - |
| 2022-04-16 | [@realhellosunsun](https://github.com/realhellosunsun) | ￥188.00
| 2022-08-30 | [@yangxiaozhe13](https://github.com/yangxiaozhe13) | ￥88.00
| 2022-09-01 | [@robot-2233](https://github.com/robot-2233) | ￥88.00
| 2023-05-09 | 埃菲尔没有塔尖 | ￥68.80
| 2023-09-21 | [@burujiuzheyang](https://github.com/burujiuzheyang) | ￥50.00
| 2023-10-07 | [@Lnine9](https://github.com/Lnine9) | ￥20.00
| 2023-10-09 | [@xiaoran-xr](https://github.com/xiaoran-xr) | ￥20.00
| 2023-10-10 | [@hsdanbai](https://github.com/hsdanbai) | ￥20.00
| 2023-10-19 | [@shuiniu86](https://github.com/shuiniu86) | ￥50.00
| 2023-10-24 | [@yuzhou6](https://github.com/yuzhou6) | ￥50.00
| 2023-11-13 | [@xuedipiaofei](https://github.com/xuedipiaofei) | ￥50.00
| 2024-01-06 | [@if-always](https://github.com/if-always) | ￥10.00
| 2024-01-21 | [@dydwgmcnl4241](https://github.com/dydwgmcnl4241) | ￥10.00
| 2024-02-18 | [@zhaolipo](https://github.com/zhaolipo) | ￥10.00
| 2024-02-19 | [@qianwangali](https://github.com/qianwangali) | ￥10.00
| 2024-02-20 | 没事干的小伙子 | ￥8.88
| 2024-02-20 | [@ning-0217](https://github.com/ning-0217) | ￥50.00
| 2024-03-08 | [@zhaolipo](https://github.com/zhaolipo) | ￥20.00
| 2024-03-18 | [@magiceric](https://github.com/magiceric) | ￥88.00

<img src="https://github.com/mouday/spider-admin-pro/raw/master/doc/img/alipay.jpg" width="300">

## 项目截图

![](https://github.com/mouday/spider-admin-pro/raw/master/doc/img/dashboard.png)

![](https://github.com/mouday/spider-admin-pro/raw/master/doc/img/project.png)

![](https://github.com/mouday/spider-admin-pro/raw/master/doc/img/schedule.png)

![](https://github.com/mouday/spider-admin-pro/raw/master/doc/img/logs.png)

## 安装升级
```
pip3 install -U spider-admin-pro -i https://pypi.org/simple
```


## Stargazers over time

[![Stargazers over time](https://starchart.cc/mouday/spider-admin-pro.svg)](https://starchart.cc/mouday/spider-admin-pro)



## 其他问题

1、windows系统 scrapyd 启动失败，可能缺少依赖pywin32

```
pip install pywin32
```

感谢[@whobywind](https://github.com/whobywind)，提供的解决方案

2、网站有ip校验，刚访问几个请求就被禁止访问？

同一个ip可能有被封的风险，可以使用代理ip去请求，有免费和付费。

如果是个人使用，可以找一些免费的ip临时使用

如果是企业项目，可以使用付费代理ip

某爬虫大佬也推荐过一个不错的动态代理 [云立方](http://www.yunlifang.cn?u=mouday)

<a href="http://www.yunlifang.cn?u=mouday" target="_blank" style="display: inline-block; background-color: #000;">
<img src="https://www.yunlifang.cn/user/img/720X90.png">
</a>

找客服发送暗号：【爬虫推广】可以获取打折优惠

具体搭建方法在大佬的博客中有详尽说明：

[使用 Tornado+Redis 维护 ADSL 拨号服务器代理池](https://cuiqingcai.com/4596.html)

如果有问题，可以加QQ群，群里的小伙伴会积极解答喔

3、为什么外网访问不到，如何修改端口号

增加`--bind` 参数

格式

```bash
--bind 监听地址:监听端口号
```

例如

```bash
# 启动运行
$ gunicorn 'spider_admin_pro:app'

# 支持外网可访问，云服务器（阿里云或腾讯云）需要设置安全组 
# 默认内网访问 --bind 127.0.0.1:8000
$ gunicorn --bind '0.0.0.0:8000' 'spider_admin_pro:app'
```

更多设置，可参考[gunicorn](https://docs.gunicorn.org/en/stable/index.html)

4、提示缺少libfile

群友 `@Yuan、红尘美` 提供的解决方法

安装依赖

```bash
yum install libffi-devel -y
```

## 更新日志

- v2.0.3
    - 修复mysql作为后端存储的文档和登录bug

- v2.0.2
    - 优化文档
    - 优化日志

- v2.0.1
    - 优化前端界面在windows平台显示异常的问题
    - 修复前端调度日志 列表显示异常的问题
    - 优化定时任务添加，自动选中项目和爬虫 

- v2.0.0
    - 升级依赖 requirements.txt， Flask 1.0.3 升级为 2.2.2
    - 优化启动方式
    - 优化启动配置,移除`PORT` 和`HOST` 配置项
    - 移除.env环境变量配置，简化配置流程
    - 移除Flask配置读取，推荐使用`gunicorn`启动服务

- 2021-09-03 
    - [bugfix]修复【任务列表】运行中项目无法取消的bug

- 2022-04-01 
    - [bugfix] 当修改scrapyd的端口号后，在配置文件中指定scrapyd为修改后的端口号。配置文件不生效
    - 感谢：@洒脱的狂者 发现的问题及解决办法

- 2022-05-27 
    - [update] requirements.txt 文件中增加 flask_cors 依赖


## 社区其他优秀工具推荐

- https://github.com/DormyMo/SpiderKeeper
- https://github.com/my8100/scrapydweb
- https://github.com/ouqiang/gocron 使用Go语言开发的轻量级定时任务集中调度和管理系统, 用于替代Linux-crontab

## Spider Admin Pro vs. Spider Admin

1. 简化了一些功能；
2. 优化了前端界面，基于Vue的组件化开发；
3. 优化了后端接口，对后端项目进行了目录划分；
4. 整体代码利于升级维护。
5. 目前仅对Python3进行了支持
6. 路由统一管理
7. 全局异常捕获
8. 接口统一返回
9. 前后端分离
10. 可视化参数配置
