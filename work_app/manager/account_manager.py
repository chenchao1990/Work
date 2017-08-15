#!/usr/bin/env python
# _*_coding:utf-8 _*_

from work_app import models
from backend.response.base_response import BaseResponse


def check_valid(**kwargs):
    response = BaseResponse()
    try:
        result = models.AdminInfo.objects.get(**kwargs)
        response.status = True
        response.data = result
    except Exception, e:
        response.message = str(e)
    return response
