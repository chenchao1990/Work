from django.contrib import admin

# Register your models here.

from idc_app import models


class PengboshiReport(admin.ModelAdmin):
    list_display = ("date", "duty_operator", "entrust_work", "SN")
admin.site.register(models.PengboshiReport, PengboshiReport)


class PengboshiBreakdown(admin.ModelAdmin):
    list_display = ("date", "manufacturer", "version", "description", "solution_state")
admin.site.register(models.PengboshiBreakdown, PengboshiBreakdown)

