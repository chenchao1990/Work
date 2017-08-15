#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import absolute_import
from celery import Celery

app = Celery('mail_send', include=['mail_send.tasks'])

app.config_from_object('mail_send.config')

if __name__ == '__main__':
    app.start()
