#!/usr/bin/env python
# _*_coding:utf-8 _*_

from work_app import models
from django.db.models import Q
from backend.response.base_response import BaseResponse
from backend.response.base_response import CreateWorkResponse
from mail_send.tasks import send_mail
from django.db import transaction
from work_app.model_handles import work_handle
from Work import settings
from collections import OrderedDict
import time


def make_order_dict(work_id):
    '''
    生成一个有序的字典
    '''
    ret = work_handle.get_work_by_work_id(work_id)

    order_dict = OrderedDict()
    order_dict[u'工单号'] = ret.work_id
    order_dict[u'创建人'] = ret.user
    order_dict['work_title'] = ret.work_title
    order_dict[u'工单类别'] = ret.operation_type
    order_dict[u'工单对象'] = ret.specific
    order_dict[u'SN'] = ret.sn
    order_dict[u'机柜'] = ret.cabinet
    order_dict[u'IDC'] = ret.idc
    order_dict[u'优先级'] = ret.priority_level
    order_dict[u'详情'] = ret.message

    return order_dict


def create_work(post_data):
    '''
    创建工单 中间处理层
    将数据字典写入库 然后将结果返回
    '''
    response = BaseResponse()

    try:
        with transaction.atomic():
            t = settings.now_time()
            post_data['add_time'] = t
            post_data['start_time'] = time.time()

            idc_id = post_data['idc_id']            # 获取idc的id 来获取邮箱地址
            idc_email = work_handle.get_idc_email(idc_id)
            idc_email = dict(idc_email).get('email')
            print "-------=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-==-==-"
            work_handle.create_new_work(post_data)      # 将工单字典传入写库方法
            print "=================create over "
            response.status = True

            if response.status:
                order_dict = make_order_dict(post_data['work_id'])

                email_msg = ""
                for key, value in order_dict.items():
                    msg_ = key + ":" + str(value) + "\n"
                    email_msg += msg_
                title = order_dict.pop('work_title')
                # send_mail_by_thread(order_dict, idc_email)
                re = send_mail.delay(title, email_msg, idc_email)
                re.ready()
    except Exception, e:
        print "mail_send mail  error ::::::::", e
        response.message = str(e)

    return response


def get_asset_lists_count(conditions):
    '''
    获取搜索到资产的个数
    '''

    # conditions = {'event_state__id': ['3']}
    response = BaseResponse()
    try:
        con = Q()
        for k, v in conditions.items():
            temp = Q()
            temp.connector = 'OR'
            for item in v:
                temp.children.append((k, item))
            con.add(temp, 'AND')
        result = work_handle.get_work_lists_q_count(con)         # j将搜索条件Q 传入其中 取出搜索到的数据的条数
        response.data = result
        response.status = True
    except Exception, e:
        response.message = str(e)

    return response


def get_to_do_lists_count(idc_id):
    '''
    获取待办的工单个数
    '''
    response = BaseResponse()
    try:
        result = work_handle.get_to_do_work_lists_count(idc_id)         # j将搜索条件Q 传入其中 取出搜索到的数据的条数
        response.data = result
        response.status = True
    except Exception, e:
        response.message = str(e)

    return response


def get_shutdown_lists_count(idc_id):
    '''
    获取关闭的工单个数
    '''
    response = BaseResponse()
    try:
        result = work_handle.get_shutdown_work_lists_count(idc_id)         # j将搜索条件Q 传入其中 取出搜索到的数据的条数
        response.data = result
        response.status = True
    except Exception, e:
        response.message = str(e)

    return response


def get_over_lists_count(idc_id):
    '''
    获取已完成工单的个数
    '''

    # conditions = {'event_state__id': ['3']}
    response = BaseResponse()
    try:

        result = work_handle.get_over_work_count(idc_id)
        response.data = result
        response.status = True
    except Exception, e:
        response.message = str(e)

    return response


def get_work_lists(conditions, page_start, page_stop):
    '''
    获取工单的简要信息
    '''
    response = BaseResponse()
    try:
        values = ['id', 'work_id', 'work_title', 'operation_type__operation', 'specific__name',  'priority_level__priority',
                  'event_state__event_type', 'user__name', 'idc__name', 'add_time', 'over_time',
                  'event_state__event_mark']      # 在这里定义好查询表时 需要筛选的字段
        con = Q()
        for k, v in conditions.items():                     # 循环搜索字典中的数据
            temp = Q()                                      # 创建一个综合搜索的对象
            temp.connector = 'OR'                           # 设置关系为OR
            for item in v:                                  # 遍历搜索字典中的value列表
                temp.children.append((k, item))
            con.add(temp, 'AND')                            # 将字典中的每种搜索条件关系设置为AND

        result = work_handle.get_work_list(page_start, page_stop, con, values)    # 搜索工单信息
        result = list(result)
        response.data = result                  # 封装到对象中
        response.status = True

    except Exception, e:
        response.message = str(e)

    return response


def get_to_do_work_lists(page_start, page_stop, idc_id):
    '''
    获取工单的简要信息
    '''
    response = BaseResponse()
    try:
        values = ['id', 'work_id', 'work_title', 'operation_type__operation', 'specific__name',  'priority_level__priority',
                  'event_state__event_type', 'user__name', 'idc__name', 'add_time', 'over_time',
                  'event_state__event_mark']      # 在这里定义好查询表时 需要筛选的字段

        result = work_handle.get_to_do_work_list(page_start, page_stop, values, idc_id)    # 搜索工单信息
        result = list(result)
        response.data = result                  # 封装到对象中
        response.status = True

    except Exception, e:
        response.message = str(e)

    return response


def get_shutdown_work_lists(page_start, page_stop, idc_id):
    '''
    获取工单的简要信息
    '''
    response = BaseResponse()
    try:
        values = ['id', 'work_id', 'work_title', 'operation_type__operation', 'specific__name',  'priority_level__priority',
                  'event_state__event_type', 'user__name', 'idc__name', 'add_time', 'over_time',
                  'event_state__event_mark']      # 在这里定义好查询表时 需要筛选的字段

        result = work_handle.get_shutdown_work_list(page_start, page_stop, values, idc_id)    # 搜索工单信息
        result = list(result)
        response.data = result                  # 封装到对象中
        response.status = True

    except Exception, e:
        response.message = str(e)

    return response


def get_over_work_lists(page_start, page_stop, idc_id):
    '''
    获取已完成工单的简要信息
    '''
    response = BaseResponse()
    try:
        values = ['id', 'work_id', 'work_title', 'operation_type__operation', 'specific__name',  'priority_level__priority',
                  'event_state__event_type', 'user__name', 'idc__name', 'add_time', 'over_time',
                  'event_state__event_mark']      # 在这里定义好查询表时 需要筛选的字段
        result = work_handle.get_over_work_list(page_start, page_stop, values, idc_id)    # 搜索工单信息
        result = list(result)
        response.data = result                  # 封装到对象中
        response.status = True

    except Exception, e:
        response.message = str(e)

    return response


def get_work_detail(nid):
    '''
    获取指定工单的详细信息
    '''
    response = BaseResponse()
    try:
        work_obj = work_handle.get_work_by_id(nid)                  # 根据id获取一条资产对象
        result = {'work_msg': work_obj}
        response.status = True
        response.data = result
    except Exception, e:
        response.message = str(e)
    return response


def get_create_work_form(login_user, work_str):
    '''
    创建工单时 需要的form表单数据
    0、工单编号 字符串
    1、登陆用户字典

    2、工单类别
    3、操作具体对象
    4、优先级
    5、工单状态  字典
    6、IDC
    '''
    response = CreateWorkResponse()
    try:
        specific_re = work_handle.get_specific()                    # 将工单类别下的 所有项获取到 并封装在字典中
        operation_re = work_handle.get_operation()                  # 将工单类别下的 所有项获取到 并封装在字典中
        priority_re = work_handle.get_priority()                        # 获取优先级
        idc_re = work_handle.get_idc()
        work_state_re = work_handle.get_work_state()                    # 获取工单状态

        response.specific_data = specific_re
        response.operate_data = list(operation_re)
        response.priority = list(priority_re)
        response.idc = list(idc_re)
        response.work_state = list(work_state_re)

        response.login_user = login_user
        response.work_str = work_str
        response.status = True
    except Exception, e:
        response.message = str(e)
    return response


def change_work_state(state_str, work_id):
    response = BaseResponse()
    try:
        if state_str == 'running':
            work_handle.change_state_by_obj(state_str, work_id)

        elif state_str == 'finish':
            work_handle.change_state_by_obj(state_str, work_id)

        elif state_str == 'shutdown':
            work_handle.change_state_by_obj(state_str, work_id)

        response.status = 1
        response.data = "OK"

    except Exception, e:
        response.message = str(e)
    return response



