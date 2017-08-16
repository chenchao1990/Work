#!/usr/bin/env python
# _*_coding:utf-8 _*_

from django.shortcuts import render,redirect
from django.shortcuts import HttpResponse
from backend.commons import JsonEncoder
from work_app.forms import work_form
from django.utils.safestring import mark_safe
from backend.auth.login_auth import login_auth
from backend.commons import pager
from work_app.manager import work_manager
from work_app.manager import comment_manager
from work_app import models
import json


def user_weight(request):
    num = int(request.weight)
    if num > 100:
        role = 'high'
    else:
        role = 'low'

    return role


def make_work_id():
    '''
    生成一个自定义的工单编号
    '''
    all_count = models.WorkMsg.objects.all().count()
    work_str = "gc-idcwork-%s" % all_count
    return work_str


@login_auth
def create_work(request):
    '''
    创建工单
    '''
    role = user_weight(request)
    if request.method == "POST":

        login_user = request.session.get('auth_user', None)         # 登录用户的ID和姓名
        user_id = json.loads(login_user)['id']

        data = dict(request.POST)
        data['user_id'] = [user_id]
        new_data_dict = {}
        for k, value in data.items():
            if k == 'message':
                new_data_dict[k] = value[0].strip()
            new_data_dict[k] = value[0]
        work_manager.create_work(new_data_dict)

        return redirect('/')
    return render(request, 'asset/create_info.html', {'username': request.username, 'weight': role})


@login_auth
def create_work_msg(request):
    '''
    获取创建工单的所有信息, 返回给前端用于创建工单form
    '''
    if request.method == "POST":

        login_user = request.session.get('auth_user', None)         # 登录用户的ID和姓名
        login_user = json.loads(login_user)
        work_str = make_work_id()                                   # 工单编号
        ret = work_manager.get_create_work_form(login_user, work_str).__dict__      # 出去具体的操作项
        result = json.dumps(ret)
        return HttpResponse(result)


@login_auth
def work_list(request):
    '''
    获取所有的工单信息 返回给前端AJax 展示到前端
    '''
    role = user_weight(request)
    if request.method == "POST":
        conditions = request.POST.get('condition', None)
        page = request.POST.get('page', None)
        idc_id = request.belong_idc             # 获取IDC的id 如果为0 说明是运维人员或者管理员
        if not conditions:
            if idc_id == 0:
                conditions = '{}'
            else:
                d = {'idc__id': [idc_id]}
                conditions = json.dumps(d)
        conditions = json.loads(conditions)
        all_count = work_manager.get_asset_lists_count(conditions)       # 按照搜索条件 去查询匹配到的数据条数
        page_info = pager.PageInfo(page, all_count.data)                # 根据传入的 页数 和 所有查询都的数据条数 去获取分页的对象
        ret = dict()
        ret['asset'] = work_manager.get_work_lists(conditions, page_info.start, page_info.end).__dict__     # 获取工单信息 封装在字典中
        ret['page'] = page_info.pager()

        ret['start'] = page_info.start                                      # 数据开始的位置
        result = json.dumps(ret)
        return HttpResponse(result)
    return render(request, 'asset/home.html', {'username': request.username, 'weight': role})


@login_auth
def work_to_do(request):
    role = user_weight(request)
    if request.method == "POST":
        page = request.POST.get('page', None)
        idc_id = request.belong_idc

        all_count = work_manager.get_to_do_lists_count(idc_id)       # 按照搜索条件 去查询匹配到的数据条数
        page_info = pager.PageInfo(page, all_count.data)                # 根据传入的 页数 和 所有查询都的数据条数 去获取分页的对象
        ret = dict()
        ret['asset'] = work_manager.get_to_do_work_lists(page_info.start, page_info.end, idc_id).__dict__     # 获取工单信息 封装在字典中
        ret['page'] = page_info.pager()

        ret['start'] = page_info.start                                      # 数据开始的位置
        result = json.dumps(ret)
        return HttpResponse(result)
    return render(request, 'asset/to_do.html', {'username': request.username, 'weight': role})


@login_auth
def work_doing(request):            # 获取正在执行的工单
    role = user_weight(request)
    if request.method == "POST":
        page = request.POST.get('page', None)
        idc_id = request.belong_idc

        all_count = work_manager.get_doing_lists_count(idc_id)       # 按照搜索条件 去查询匹配到的数据条数
        page_info = pager.PageInfo(page, all_count.data)                # 根据传入的 页数 和 所有查询都的数据条数 去获取分页的对象
        ret = dict()
        ret['asset'] = work_manager.get_doing_work_lists(page_info.start, page_info.end, idc_id).__dict__     # 获取工单信息 封装在字典中
        ret['page'] = page_info.pager()

        ret['start'] = page_info.start                                      # 数据开始的位置
        result = json.dumps(ret)
        return HttpResponse(result)
    return render(request, 'asset/doing_work.html', {'username': request.username, 'weight': role})


@login_auth
def work_shutdown(request):
    role = user_weight(request)
    # 获取状态为关闭的工单
    if request.method == "POST":
        page = request.POST.get('page', None)
        idc_id = request.belong_idc

        all_count = work_manager.get_shutdown_lists_count(idc_id)       # 按照搜索条件 去查询匹配到的数据条数
        page_info = pager.PageInfo(page, all_count.data)                # 根据传入的 页数 和 所有查询都的数据条数 去获取分页的对象
        ret = dict()
        ret['asset'] = work_manager.get_shutdown_work_lists(page_info.start, page_info.end, idc_id).__dict__     # 获取工单信息 封装在字典中
        ret['page'] = page_info.pager()

        ret['start'] = page_info.start                                      # 数据开始的位置
        result = json.dumps(ret)
        return HttpResponse(result)
    return render(request, 'asset/shut_down_work.html', {'username': request.username, 'weight': role})


@login_auth
def over_work(request):
    '''
    获取已完成工单页面
    '''
    role = user_weight(request)
    if request.method == 'POST':

        page = request.POST.get('page', None)
        idc_id = request.belong_idc

        all_count = work_manager.get_over_lists_count(idc_id)     # 按照搜索条件 去查询匹配到的数据条数
        page_info = pager.PageInfo(page, all_count.data)                # 根据传入的 页数 和 所有查询都的数据条数 去获取分页的对象
        ret = dict()
        ret['asset'] = work_manager.get_over_work_lists(page_info.start, page_info.end, idc_id).__dict__     # 获取工单信息 封装在字典中
        ret['page'] = page_info.pager()
        ret['start'] = page_info.start
        result = json.dumps(ret)
        return HttpResponse(result)
    return render(request, 'asset/finish_work_list.html', {'username': request.username, 'weight': role})


@login_auth
def work_to_do_list(request):
    '''
    获取所有 待办 的工单信息，返回给前端AJax 展示到前端
    '''

    page = request.POST.get('page', None)
    idc_id = request.belong_idc
    all_count = work_manager.get_to_do_lists_count(idc_id)       # 按照搜索条件 去查询匹配到的数据条数
    page_info = pager.PageInfo(page, all_count.data)                # 根据传入的 页数 和 所有查询都的数据条数 去获取分页的对象
    ret = dict()
    ret['asset'] = work_manager.get_to_do_work_lists(page_info.start, page_info.end, idc_id).__dict__     # 获取工单信息 封装在字典中
    ret['page'] = page_info.pager()

    ret['start'] = page_info.start                                      # 数据开始的位置
    result = json.dumps(ret)
    return HttpResponse(result)


@login_auth
def work_detail(request, nid):
    num = int(request.weight)

    if num > 100:
        role = 'high'
    else:
        role = 'low'
    basic = work_manager.get_work_detail(nid=nid)
    return render(request, 'asset/detail.html', {'work_message': basic, 'weight': role, 'username': request.username})


@login_auth
def get_work_state(request):
    '''
    获取工单状态
    '''
    work_num = request.POST.get('work_num')
    work_state = models.WorkMsg.objects.filter(id=work_num).values('event_state__event_mark', 'event_state__event_type')
    work_data = work_state[0]
    return HttpResponse(json.dumps(work_data))


@login_auth
def change_work_state(request):
    '''
    切换工单状态
    '''

    state_str = request.POST.get('change_value').strip()
    work_id = request.POST.get('work_id')

    ret = work_manager.change_work_state(state_str, work_id).__dict__
    return HttpResponse(json.dumps(ret))


@login_auth
def get_over_work(request):
    '''
    获取所有的工单信息 返回给前端AJax 展示到前端
    '''

    page = request.POST.get('page', None)
    all_count = work_manager.get_over_lists_count()     # 按照搜索条件 去查询匹配到的数据条数
    page_info = pager.PageInfo(page, all_count.data)                # 根据传入的 页数 和 所有查询都的数据条数 去获取分页的对象
    ret = dict()
    ret['asset'] = work_manager.get_over_work_lists(page_info.start, page_info.end).__dict__     # 获取工单信息 封装在字典中
    ret['page'] = page_info.pager()
    ret['start'] = page_info.start
    result = json.dumps(ret)
    return HttpResponse(result)


@login_auth
def get_work_msg(request):
    '''
    获取某个工单下的消息追踪
    '''
    if request.method == "POST":
        work_id = request.POST.get('work_id')
        ret = comment_manager.get_work_massage(work_id).__dict__
        return HttpResponse(json.dumps(ret))


@login_auth
def submit_work_msg(request):
    '''
    提交用户输入的 对话内容
    '''
    if request.method == "POST":
        login_user = request.session.get('auth_user', None)         # 登录用户的ID和姓名
        login_user = json.loads(login_user)['id']
        work_id = request.POST.get('work_id')
        work_msg = request.POST.get('work_msg')
        ret = comment_manager.add_work_massage(work_id, login_user, work_msg).__dict__
        return HttpResponse(json.dumps(ret))


@login_auth
def doing_work(request):
    # 待办工单
    # 将未完成的工单统一提取 返回前端
    pass




























