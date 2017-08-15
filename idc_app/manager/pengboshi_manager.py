#!/usr/bin/env python
# _*_coding:utf-8 _*_

from backend.response.base_response import BaseResponse
from idc_app.model_handles import pengboshi_handle


def get_report(month_num):
    '''
    获取某个月份的运维报告数据
    '''
    response = BaseResponse()

    try:
        ret = pengboshi_handle.get_report_by_month(month_num)
        response.status = True
        response.data = list(ret)
        return response
    except Exception, e:
        response.message = str(e)
        return response