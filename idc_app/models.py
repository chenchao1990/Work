#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import unicode_literals

from django.db import models

# Create your models here.


class PengboshiReport(models.Model):
    '''
    鹏博士每日运维报告
    '''
    month = models.CharField(u'月份', max_length=10, blank=True, null=True)
    date = models.CharField(u'日期', max_length=32, blank=True, null=True)
    duty_operator = models.CharField(u'值班人员', max_length=32, blank=True, null=True)
    check_times = models.IntegerField(u'巡检次数', blank=True, null=True)
    entrust_work = models.CharField(u'客户委托作业', max_length=160, blank=True, null=True)
    SN = models.CharField(u'SN', max_length=160, blank=True, null=True)
    person_in_out = models.IntegerField(u'人员进出', blank=True, null=True)
    device_in_out = models.IntegerField(u'设备进出', blank=True, null=True)
    breakdown_out_in = models.IntegerField(u'故障申报', blank=True, null=True)
    entrust_times = models.IntegerField(u'委托作业次数', blank=True, null=True)

    def __unicode__(self):
        return "%s %s %s " % (self.date, self.duty_operator, self.entrust_work)

    class Meta:
        verbose_name_plural = "鹏博士每日运维报告"


class PengboshiBreakdown(models.Model):
    '''
    鹏博士故障统计
    '''
    GENDER_CHOICE = (
        (u'1', u'HP'),
        (u'2', u'IBM'),
        (u'3', u'Dell'),
        (u'4', u'EMC'),
        (u'5', u'浪潮'),
        (u'6', u'联想'),
        (u'7', u'华为'),
        (u'8', u'DELL刀箱'),
    )
    month = models.CharField(u'月份', max_length=10, blank=True, null=True)
    date = models.CharField(u'故障日期', max_length=32, blank=True, null=True)
    manufacturer = models.CharField('厂商', max_length=2, choices=GENDER_CHOICE)
    version = models.CharField(u'型号', max_length=32, blank=True, null=True)
    id_key = models.CharField(u'序列号', max_length=32, blank=True, null=True)
    description = models.CharField(u'故障说明', max_length=60, blank=True, null=True)
    spare_part_info = models.CharField(u'备件具体信息', max_length=80, blank=True, null=True)
    solution_state = models.CharField(u'解决状态', max_length=32, blank=True, null=True)
    idc = models.CharField(u'机房', max_length=16, blank=True, null=True)
    cabinet = models.CharField(u'机柜', max_length=10, blank=True, null=True)
    u_slot = models.CharField(u'U位', max_length=10, blank=True, null=True)
    comment = models.CharField(u'备注', max_length=100, blank=True, null=True)
    finish_time = models.CharField(u'故障解决时间', max_length=100, blank=True, null=True)

    class Meta:
        verbose_name_plural = "鹏博士故障统计"
