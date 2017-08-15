#!/usr/bin/env python
# _*_coding:utf-8 _*_

from django import forms
from work_app import models


class UserInfo(forms.Form):

    username = forms.CharField(error_messages={'required': u"用户名不能为空"},
                               widget=forms.TextInput(attrs={'placeholder': u'用户名',
                                                             'class': "form-control", }

                                                  ),

                           )
    password = forms.CharField(error_messages={'required': u"密码不能为空"},
                               widget=forms.PasswordInput(attrs={'placeholder': u'密码',
                                                                 'class': "form-control"}
                                                      ),
                               )


# class UserInfo(forms.ModelForm):
#     class Meta:
#         model = models.User
#         fields = ('name', 'password')
#
#         widgets = {
#             'name': forms.TextInput(attrs={'class': "form-control", 'placeholder': "用户名"}),
#             'password': forms.PasswordInput(attrs={'class': "form-control",'placeholder': "密码"}),
#         }
