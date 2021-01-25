# -*- coding: utf-8 -*-
from datetime import datetime

# 常量
from apscheduler.schedulers.base import STATE_STOPPED, STATE_RUNNING, STATE_PAUSED


class SchedulerUtil(object):
    DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

    @classmethod
    def job_to_dict(cls, job):
        if hasattr(job, "next_run_time"):
            next_run_time = job.next_run_time
        else:
            next_run_time = None

        if isinstance(next_run_time, datetime):
            next_run_time = next_run_time.strftime(cls.DATETIME_FORMAT)

        if next_run_time:
            status = cls.get_state_name(STATE_RUNNING)
        else:
            status = cls.get_state_name(STATE_PAUSED)

        return {
            'id': job.id,
            'args': job.args,
            'kwargs': job.kwargs,
            'name': job.name,
            'next_run_time': next_run_time,
            'status': status
        }

    @classmethod
    def jobs_to_dict(cls, jobs):
        return [cls.job_to_dict(job) for job in jobs]

    @classmethod
    def get_state_name(cls, state):
        mapping = {
            STATE_STOPPED: 'stopped',
            STATE_RUNNING: 'running',
            STATE_PAUSED: 'paused'
        }
        return mapping[state]
