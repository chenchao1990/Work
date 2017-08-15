#!/usr/bin/env python
# _*_coding:utf-8 _*_

from work_app import models


def get_comment_count_by_id(work_id):
    '''
    获取工单的对话
    '''

    ret = models.WorkMsg.objects.filter(id=work_id).first().comment_set.all().count()
    return ret


def get_comment(work_id, value_list):
    '''
    获取工单的对话
    '''

    ret = models.WorkMsg.objects.filter(id=work_id).first().comment_set.order_by('id').values(*value_list)

    return ret


def add_comment(data_dict):
    '''
    获取工单的对话
    '''

    ret = models.Comment.objects.create(**data_dict)
    return ret












