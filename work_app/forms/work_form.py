#!/usr/bin/env python
# _*_coding:utf-8 _*_

from django import forms
from work_app import models


class NewWork(forms.Form):

    work_id = forms.CharField(
            required=False,
            widget=forms.TextInput(attrs={'class': 'form-control',                             # 工单编号
                                          'placeholder': u'必填',
                                          })
                           )

    sn = forms.CharField(
            required=False,
            widget=forms.TextInput(attrs={'class': 'form-control',                             # sn号

                                          'placeholder': u'可选',
                                          })
                           )
    cabinet = forms.CharField(
            required=False,
            widget=forms.TextInput(attrs={'class': 'form-control',                        # 机柜
                                          'placeholder': u'可选',
                                          })
                           )
    operation_type_id = forms.IntegerField(widget=forms.Select(attrs={'class': 'form-control'}))           # 操作类型
    priority_level_id = forms.IntegerField(widget=forms.Select(attrs={'class': 'form-control'}))           # 优先级
    event_state_id = forms.IntegerField(widget=forms.Select(attrs={'class': 'form-control'}))              # 事件状态
    idc_id = forms.IntegerField(widget=forms.Select(attrs={'class': 'form-control'}))            # IDC
    # operation_group_id = forms.IntegerField(widget=forms.Select(attrs={'class': 'form-control'}))          # 操作组
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',
                                                           'placeholder': u'必填',
                                                           'style': 'height: 400px;'})     # 工作信息
                              )

    def __init__(self, *args, **kwargs):
        super(NewWork, self).__init__(*args, **kwargs)
        self.fields['operation_type_id'].widget.choices = models.OperationType.objects.all().order_by('id').values_list('id', 'operation')
        self.fields['priority_level_id'].widget.choices = models.PriorityType.objects.all().order_by('id').values_list('id', 'priority')
        self.fields['event_state_id'].widget.choices = models.EventState.objects.all().order_by('id').values_list('id', 'event_type')
        self.fields['idc_id'].widget.choices = models.IDC.objects.all().order_by('id').values_list('id', 'name')
        # self.fields['operation_group_id'].widget.choices = models.Department.objects.all().order_by('id').values_list('id', 'name')
