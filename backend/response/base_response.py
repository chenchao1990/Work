#!/usr/bin/env python
# _*_coding:utf-8 _*_


class BaseResponse(object):
    def __init__(self):
        self.work_state = None
        self.status = False
        self.message = ''
        self.data = None


class CreateWorkResponse(object):
    def __init__(self):
        self.status = False
        self.message = ''
        self.work_str = None                        # 工单编号
        self.login_user = None
        self.specific_data = None
        self.operate_data = None
        self.priority = None
        self.idc = None
        self.work_state = None

