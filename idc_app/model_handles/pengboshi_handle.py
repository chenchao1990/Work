#!/usr/bin/env python
# _*_coding:utf-8 _*_

from idc_app import models


def get_report_by_month(mon_num):
    '''
    根据月份获取数据
    '''
    ret = models.PengboshiReport.objects.filter(month=mon_num).order_by('id').values()
    return ret





