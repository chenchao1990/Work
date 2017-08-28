#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.contrib import admin

# Register your models here.

from work_app import models

admin.site.register(models.OperationType)
admin.site.register(models.OperateSpecific)
admin.site.register(models.PriorityType)
admin.site.register(models.IDC)
admin.site.register(models.Comment)


class EventState(admin.ModelAdmin):
    list_display = ("event_type", "event_mark")
admin.site.register(models.EventState, EventState)


class WorkMsg(admin.ModelAdmin):
    list_display = ("work_id", "operation_type", 'specific', "priority_level", "mail_re", "user", "add_time")
admin.site.register(models.WorkMsg, WorkMsg)


class UserInfo(admin.ModelAdmin):
    list_display = ("user_type", "name", "email", "mobile")
admin.site.register(models.UserInfo, UserInfo)


class AdminInfo(admin.ModelAdmin):
    list_display = ("username",)
admin.site.register(models.AdminInfo, AdminInfo)


class UserType(admin.ModelAdmin):
    list_display = ("caption", "code")
admin.site.register(models.UserType, UserType)


