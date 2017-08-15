#!/usr/bin/env python
# _*_coding:utf-8 _*_

from work_app import models
from backend.response.base_response import BaseResponse
from django.db import transaction
from work_app.model_handles import work_handle
from work_app.model_handles import comment_handle
from Work import settings
import time


def get_work_massage(work_id):
    '''
    获取工单的对话  根绝工单ID
    '''
    response = BaseResponse()
    values = ['id', 'user_from__name', 'message', 'submit_time']
    try:
        work_state = list(work_handle.get_work_state_by_id(work_id))[0]

        msg_obj = list(comment_handle.get_comment(work_id, values))

        response.status = True
        response.data = msg_obj
        response.work_state = work_state
    except Exception, e:
        print "get_work_msg_______error", e
        response.message = str(e)

    return response


def add_work_massage(work_id, user_id, work_msg):
    '''
    获取工单的对话  根绝工单ID
    '''
    response = BaseResponse()
    if len(work_msg.strip()) == 0:
        response.status = True
        response.data = 1
        return response
    try:
        with transaction.atomic():
            work_msg.replace('\r\n', '<br />')
            data_dict = {}
            t = settings.now_time()
            data_dict['user_from_id'] = user_id
            data_dict['work_from_id'] = work_id
            data_dict['message'] = work_msg
            data_dict['submit_time'] = t
            comment_handle.add_comment(data_dict)
            response.status = True
            response.data = 1
    except Exception, e:
        print "create_______error", e
        response.message = str(e)

    return response

