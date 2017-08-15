#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render, redirect

# Create your views here.
from work_app.forms import user_form
from work_app.manager import account_manager

import json


def login(request):
    error = ''
    login_form = user_form.UserInfo(request.POST)
    if request.method == "POST":
        if not login_form.is_valid():
            error = '用户名或密码格式错误.'
        else:
            data = login_form.clean()
            result = account_manager.check_valid(**data)        # 专门检测用户登录账户密码的方法
            if result.status:
                user_type_code = result.data.user_info.user_type.code
                ret = {'id': result.data.user_info.id,              # 获取用户的id
                       'name': result.data.user_info.name,          # 获取用户的名称
                       'weight': user_type_code,        # 获取用户所属类型的权重
                       }
                if user_type_code == "100":             # 这是IDC人员
                    ret['belong_idc'] = result.data.user_info.belong_idc.id
                else:
                    ret['belong_idc'] = 0
                request.session['auth_user'] = json.dumps(ret)
                target = request.GET.get('back', '/')
                print "Login  successful!!!!!!", target
                return redirect(target)

            else:
                error = '用户名或密码错误.'

    return render(request, 'auth/login.html', {'error': error, 'login_obj': login_form})


def logout(request):
    del request.session['auth_user']
    request.username = ''
    return redirect('/account/login/')




