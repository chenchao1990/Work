#!/usr/bin/env python
# _*_coding:utf-8 _*_

from work_app import models


def idc_id_is0(num):
    if num == 0:
        return True
    else:
        return False


def create_new_work(value_dict):
    '''
    根据字典来创建一个新工单
    '''
    ret = models.WorkMsg.objects.create(**value_dict)
    return ret


def get_idc_email(idc_id):
    '''
    根据idc_id来获取idc邮箱
    '''
    ret = models.IDC.objects.filter(id=2).values('email').first()
    return ret


def get_work_list(start, end, condition, values):
    try:
        ret = models.WorkMsg.objects.filter(condition).order_by('-id').values(*values)[start:end]
        return ret
    except Exception, e:
        print "get__all__work_err", e
        return str(e)


def get_to_do_work_list(start, end, values, idc_id):
    try:
        if idc_id_is0(idc_id):
            d = {'event_state__event_mark': 'wait'}
        else:
            d = {'event_state__event_mark': 'wait', 'idc__id': idc_id}

        ret = models.WorkMsg.objects.filter(**d).order_by('-id').values(*values)[start:end]
        return ret
    except Exception, e:
        print "get_wait__work_err", e
        return str(e)


def get_doing_work_list(start, end, values, idc_id):
    try:
        if idc_id_is0(idc_id):
            d = {'event_state__event_mark': 'running'}
        else:
            d = {'event_state__event_mark': 'running', 'idc__id': idc_id}

        ret = models.WorkMsg.objects.filter(**d).order_by('-id').values(*values)[start:end]
        return ret
    except Exception, e:
        print "get__doing__work_err: ", e
        return str(e)


def get_over_work_list(start, end, values, idc_id):
    try:
        if idc_id_is0(idc_id):
            d = {'event_state__event_mark': 'finish'}
        else:
            d = {'event_state__event_mark': 'finish', 'idc__id': idc_id}

        ret = models.WorkMsg.objects.filter(**d).order_by('-id').values(*values)[start:end]
        return ret
    except Exception, e:
        print "get__over__work_err", e
        return str(e)


def get_shutdown_work_list(start, end, values, idc_id):
    try:
        if idc_id_is0(idc_id):
            d = {'event_state__event_mark': 'shutdown'}
        else:
            d = {'event_state__event_mark': 'shutdown', 'idc__id': idc_id}

        ret = models.WorkMsg.objects.filter(**d).order_by('-id').values(*values)[start:end]
        return ret
    except Exception, e:
        print "get__shutdown__work_err", e
        return str(e)


def get_work_lists_q_count(condition):
    # condition 为用户输入的搜索条件 经过进一步处理合成的Q
    ret = models.WorkMsg.objects.filter(condition).count()
    return ret


def get_to_do_work_lists_count(idc__id):
    # 获取待办工单个数
    if idc_id_is0(idc__id):
        d = {'event_state__event_mark': 'wait'}
    else:
        d = {'event_state__event_mark': 'wait', 'idc__id': idc__id}
    ret = models.WorkMsg.objects.filter(**d).count()
    return ret


def get_doing_work_lists_count(idc__id):
    # 获取执行中工单个数
    if idc_id_is0(idc__id):
        d = {'event_state__event_mark': 'running'}
    else:
        d = {'event_state__event_mark': 'running', 'idc__id': idc__id}
    ret = models.WorkMsg.objects.filter(**d).count()
    return ret


def get_shutdown_work_lists_count(idc_id):

    # 获取待办工单个数
    if idc_id_is0(idc_id):
        d = {'event_state__event_mark': 'shutdown'}
    else:
        d = {'event_state__event_mark': 'shutdown', 'idc__id': idc_id}
    ret = models.WorkMsg.objects.filter(**d).count()
    return ret


def get_over_work_count(idc_id):
    # 获取已完成的工单
    if idc_id_is0(idc_id):
        d = {'event_state__event_mark': 'finish'}
    else:
        d = {'event_state__event_mark': 'finish', 'idc__id': idc_id}
    ret = models.WorkMsg.objects.filter(**d).count()
    return ret


def get_work_by_id(work_id):
    '''
    根据ID 获取工单
    '''
    ret = models.WorkMsg.objects.filter(id=work_id).first()
    return ret


def get_work_by_work_id(work_id):
    '''
    根据work id 获取工单
    '''
    ret = models.WorkMsg.objects.filter(work_id=work_id).first()
    return ret


def get_operation_type():
    '''
    获取工单类别字段
    '''
    ret = models.OperationType.objects.all().order_by('id').values(['id', 'operation'])
    return ret


def get_specific():
    '''
    获取具体操作对象数据
    :return:
    '''
    re_dict = {}
    feild_dict = {
        'hardware': 9,
        'os': 10,
        'implement': 11,
        'collect': 12,
        'part_manage': 13,
        'other': 14,
    }

    operate_id = models.OperationType.objects.all().values('id')           # 获取工单类别的所有id
    all_id_list = []
    for value in list(operate_id):
        all_id_list.append(int(value['id']))
    for i in all_id_list:                        # 根据工单类别的id 去获取各自的 操作对象

        ret = models.OperateSpecific.objects.filter(name_belong__id=i).order_by('id').values('id', 'name')
        re_dict[i] = list(ret)

    return re_dict


def get_operation():
    '''
    获取工单类别
    '''
    ret = models.OperationType.objects.all().order_by('id').values('id', 'operation', 'tag')
    return ret


def get_priority():
    '''
    获取优先级数据
    '''
    ret = models.PriorityType.objects.all().order_by('id').values('id', 'priority')
    return ret


def get_work_state():
    '''
    :return: 获取工单的状态
    '''
    values = ['id', 'event_type', 'event_mark']
    ret = models.EventState.objects.all().order_by('id').values(*values)
    return ret


def get_work_state_by_id(work_id):
    '''
    :return: 获取工单的状态
    '''
    ret = models.WorkMsg.objects.filter(id=work_id).values('event_state__event_mark')
    return ret


def get_idc():
    '''
    获取IDC的数据
    :return:
    '''
    ret = models.IDC.objects.all().order_by('id').values('id', 'name')
    return ret


def change_state_by_obj(state_str, work_id):
    state_obj = models.EventState.objects.filter(event_mark=state_str).first()
    msg_obj = models.WorkMsg.objects.filter(id=work_id).first()
    msg_obj.event_state = state_obj
    msg_obj.save()
