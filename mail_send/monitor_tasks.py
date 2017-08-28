#!/usr/bin/env python
# _*_coding:utf-8 _*_

from __future__ import absolute_import
from mail_send.celery import app
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import redis
import time
import json
import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Work.settings")
django.setup()
from work_app.model_handles.work_handle import update_mail_result


@app.task
def get_task_re(task_id):
    r = redis.Redis(host='localhost', port='6379', db=5)
    for i in range(2):
        v = r.get(task_id)
        if v:
            s = json.loads(v)
            update_mail_result(task_id, s['result'])

        time.sleep(8)

