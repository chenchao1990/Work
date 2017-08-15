#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import unicode_literals

from django.db import models

# Create your models here.


class UserType(models.Model):
    '''
    用户类型
    '''
    caption = models.CharField(max_length=32, db_index=True, unique=True)
    code = models.CharField(max_length=32, db_index=True, unique=True)

    def __unicode__(self):
        return self.caption

    class Meta:
        verbose_name_plural = "用户类型"


class UserInfo(models.Model):
    '''
    用户的基本信息
    '''
    user_type = models.ForeignKey('UserType')
    name = models.CharField(u'名字', max_length=64, blank=False, null=False)
    email = models.EmailField(u'邮箱', blank=False, null=False )
    mobile = models.CharField(u'手机', max_length=32, null=True, blank=True)
    user_auth = models.IntegerField(u'用户权限', null=True, blank=True)
    belong_idc = models.ForeignKey('IDC', null=True, blank=True)

    class Meta:
        verbose_name_plural = "用户信息"

    def __unicode__(self):
        return self.name


class AdminInfo(models.Model):
    '''
    用户登陆账号
    '''
    user_info = models.OneToOneField('UserInfo')
    username = models.CharField(u'用户名', max_length=256)
    password = models.CharField(u'密码', max_length=256)

    class Meta:
        verbose_name_plural = "用户登陆账号"


class IDC(models.Model):
    '''
    IDC机房信息
    '''
    name = models.CharField(u'IDC', max_length=72)
    email = models.EmailField(u'邮箱')

    class Meta:
        verbose_name_plural = "IDC"

    def __unicode__(self):
        return self.name


class EventState(models.Model):
    '''
    工单状态
    '''
    event_type = models.CharField(max_length=120)                        # 工单状态
    event_mark = models.CharField(max_length=60)                         # 工单状态记号

    def __unicode__(self):                      # 这里修改的是在admin里的表里
        return u'%s ' % self.event_type

    class Meta:                                 # 这里修改的是在admin里面的表名称
        verbose_name_plural = "工单状态"


class PriorityType(models.Model):
    '''
    优先级
    '''
    priority = models.CharField(max_length=120, unique=True, blank=True, null=True)              # 优先级

    def __unicode__(self):                      # 这里修改的是在admin里的表里
        return u'%s' % self.priority

    class Meta:                                 # 这里修改的是在admin里面的表名称
        verbose_name_plural = "优先级"


class OperationType(models.Model):
    '''
    操作类型
    '''
    operation = models.CharField(max_length=120, unique=True, blank=False, null=False)              # 工单类别
    tag = models.CharField(max_length=32, unique=True, blank=True, null=True)

    def __unicode__(self):                      # 这里修改的是在admin里的表里
        return u'%s' % self.operation

    class Meta:                                 # 这里修改的是在admin里面的表名称
        verbose_name_plural = "工单类别"


class OperateSpecific(models.Model):
    '''
    具体的操作对象     [spɪˈsɪfɪk]
    '''
    name = models.CharField(u'具体操作对象', max_length=120, unique=True, blank=False, null=False)
    name_belong = models.ForeignKey('OperationType')
    tag = models.CharField(max_length=32, unique=True, blank=True, null=True)

    def __unicode__(self):                      # 这里修改的是在admin里的表里
        return u'%s' % self.name

    class Meta:                                 # 这里修改的是在admin里面的表名称
        verbose_name_plural = "具体操作项"


class WorkMsg(models.Model):
    '''
    工单表
    '''
    work_id = models.CharField(max_length=120, unique=True, blank=False, null=False)        # 工单编号
    user = models.ForeignKey('UserInfo', blank=True, null=True)                             # 申请人
    work_title = models.CharField(max_length=120)                                           # 文章的标题
    jira_id = models.CharField(max_length=60, blank=True, null=True)                        # jira编号
    sn = models.CharField(max_length=120, blank=True, null=True)                            # SN号
    cabinet = models.CharField(max_length=120, blank=True, null=True)                       # 机柜
    operation_type = models.ForeignKey('OperationType', null=False, blank=False)            # 工单类别
    specific = models.ForeignKey('OperateSpecific', null=False, blank=False)                # 操作具体对象
    priority_level = models.ForeignKey('PriorityType', null=False, blank=False)             # 优先级
    event_state = models.ForeignKey('EventState', null=True, blank=True)                    # 工单状态
    message = models.TextField(max_length=1200, blank=True, null=True)                      # 工单信息
    idc = models.ForeignKey('IDC')                                                          # IDC
    add_time = models.CharField(max_length=120, blank=True, null=True)                      # 申请时间
    over_time = models.CharField(max_length=120, blank=True, null=True)                     # 完成时间
    start_time = models.CharField(max_length=32, blank=True, null=True)                     # 开始时间戳
    stop_time = models.CharField(max_length=32, blank=True, null=True)                      # 结束时间戳

    def __unicode__(self):                      # 这里修改的是在admin里的表里
        return u'%s %s %s %s %s' % (self.idc, self.operation_type, self.event_state, self.message, self.add_time)

    class Meta:                                 # 这里修改的是在admin里面的表名称
        verbose_name_plural = "工单信息"


class Comment(models.Model):
    '''
    工单的问题交流
    '''
    user_from = models.ForeignKey('UserInfo')                           # 所属用户
    work_from = models.ForeignKey('WorkMsg')                            # 所属工单
    message = models.TextField(blank=True, null=True)                   # 对话内容
    submit_time = models.CharField(max_length=120, blank=True, null=True)   # 提交时间

    def __unicode__(self):                      # 这里修改的是在admin里的表里
        return u'%s %s %s' % (self.work_from, self.user_from, self.submit_time,)

    class Meta:                                 # 这里修改的是在admin里面的表名称
        verbose_name_plural = "工单对话"


















































