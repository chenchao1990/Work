#!/usr/bin/env python
# _*_coding:utf-8 _*_

from django.shortcuts import render,redirect
from django.shortcuts import HttpResponse
from backend.auth.login_auth import login_auth
from idc_app.manager import pengboshi_manager
import json
import datetime

@login_auth
def detail_list(request):
    '''
    展示鹏博士机房信息
    '''

    return render(request, 'idc/pengboshi.html')


@login_auth
def pengboshi_report(request):
    '''
    按月份获取运维数据
    '''

    if request.method == 'POST':
        s = datetime.datetime.now()
        month_num = request.POST.get('month_num')
        print "month__________________________num", month_num
        if month_num:       # 有月份的参数
            print "have Month num>>>>>>>>>>>>>>>>>>>>>>"
            ret = pengboshi_manager.get_report(int(month_num)).__dict__
            return HttpResponse(json.dumps(ret))

        else:               # 无月份的参数
            print "No Month num>>>>>>>>>>>>>>>>>>>>>>"
            ret = pengboshi_manager.get_report(s.month).__dict__
            return HttpResponse(json.dumps(ret))


@login_auth
def pengboshi_breakdown(request):
    '''
    鹏博士故障统计
    '''

    if request.method == 'POST':
        s = datetime.datetime.now()
        month_num = request.POST.get('month_num')
        print "month__________________________num", month_num
        if month_num:       # 有月份的参数
            print "have Month num>>>>>>>>>>>>>>>>>>>>>>"
            ret = pengboshi_manager.get_report(int(month_num)).__dict__
            return HttpResponse(json.dumps(ret))

        else:               # 无月份的参数
            print "No Month num>>>>>>>>>>>>>>>>>>>>>>"
            ret = pengboshi_manager.get_report(s.month).__dict__
            return HttpResponse(json.dumps(ret))

