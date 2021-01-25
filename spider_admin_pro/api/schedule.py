# -*- coding: utf-8 -*-
# ==============================================
# 调度器接口服务
# ==============================================

from flask import request

from spider_admin_pro.lib.flask_app.flask_app import BlueprintAppApi
from spider_admin_pro.lib.scheduler.scheduler_util import SchedulerUtil
from spider_admin_pro.model.history import HistoryModel
from spider_admin_pro.service.auth import AuthService
from spider_admin_pro.service.scheduler_service import SchedulerService, scheduler

schedule_api = BlueprintAppApi(name="schedule", import_name=__name__)


@schedule_api.before_request
def before_request():
    token = request.headers.get('Token')

    AuthService.check_token(token)


#########################
#   任务管理
#########################
@schedule_api.post("/getJobs")
def get_jobs():
    jobs = scheduler.get_jobs()
    return SchedulerUtil.jobs_to_dict(jobs)


@schedule_api.post("/addJob")
def add_job():
    """任务修改成功
    job_id  定时任务id, str 可选，存在则更新，没有则新增
    project 项目名 str
    spider  爬虫名 str
    cron    cron表达式 eg: 分 时 日 月 周（* * * * *）
    options 其他参数 json
        eg: '{"setting": "DOWNLOAD_DELAY=2", "jobid": "xxx", "_version": 123456}'
    """
    project = request.json['project']
    spider = request.json['spider']
    cron = request.json['cron']

    job_id = request.json.get('job_id')
    options = request.json.get('options')

    SchedulerService.add_job(
        project=project, spider=spider, cron=cron,
        options=options, job_id=job_id
    )


@schedule_api.post("/removeJob")
def remove_job():
    """任务移除"""
    job_id = request.json['job_id']
    scheduler.remove_job(job_id=job_id)


@schedule_api.post("/pauseJob")
def pause_job():
    """暂停成功"""
    job_id = request.json['job_id']
    scheduler.pause_job(job_id=job_id)


@schedule_api.post("/resumeJob")
def resume_job():
    """继续运行"""
    job_id = request.json['job_id']
    scheduler.resume_job(job_id=job_id)


@schedule_api.post("/jobDetail")
def job_detail():
    job_id = request.json["job_id"]
    job = scheduler.get_job(job_id)
    return SchedulerUtil.job_to_dict(job)


#########################
#   调度器管理
#########################
@schedule_api.post("/start")
def start():
    """启动调度"""
    scheduler.start()


@schedule_api.post("/state")
def state():
    """查看状态"""
    return {
        'state': SchedulerUtil.get_state_name(scheduler.state)
    }


@schedule_api.post("/shutdown")
def shutdown():
    """关闭调度"""
    scheduler.shutdown()


@schedule_api.post("/pause")
def pause():
    """全部任务暂停"""
    scheduler.pause()


@schedule_api.post("/resume")
def resume():
    """全部任务继续"""
    scheduler.resume()


@schedule_api.post("/removeAllJobs")
def remove_all_jobs():
    """全部任务移除"""
    scheduler.remove_all_jobs()


# ==============================================
# 调度日志
# ==============================================

@schedule_api.post("/scheduleLogs")
def schedule_logs():
    """调度日志"""
    page = request.json.get("page", 1)
    size = request.json.get("size", 20)
    status = request.json.get("status")
    project = request.json.get("project")
    spider = request.json.get("spider")
    schedule_job_id = request.json.get("schedule_job_id")

    return {
        'list': SchedulerService.get_log_list(page=page, size=size, status=status, project=project, spider=spider,
                                              schedule_job_id=schedule_job_id),
        'total': SchedulerService.get_log_total_count(project=project, spider=spider, schedule_job_id=schedule_job_id),
        'success': SchedulerService.get_log_success_count(project=project, spider=spider,
                                                          schedule_job_id=schedule_job_id),
        'error': SchedulerService.get_log_error_count(project=project, spider=spider, schedule_job_id=schedule_job_id),
    }


@schedule_api.post("/removeScheduleLogs")
def remove_schedule_logs():
    """调度日志"""
    status = request.json.get("status")
    project = request.json.get("project")
    spider = request.json.get("spider")
    schedule_job_id = request.json.get("schedule_job_id")

    res = SchedulerService.remove_log(project=project, spider=spider, schedule_job_id=schedule_job_id, status=status)
    print(res)
