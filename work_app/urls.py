"""Moment URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from work_app.views import home
from work_app.views import work
from work_app.views import account

urlpatterns = [
    url(r'all_work/$', work.work_list),
    url(r'^$', work.work_to_do),
    url(r'login/$', account.login),
    url(r'logout/$', account.logout),

    url(r'create_work/$', work.create_work),
    url(r'get_work_form/$', work.create_work_msg),
    url(r'work_list/$', work.work_list),
    url(r'work/detail/(?P<nid>\d*)$', work.work_detail),
    url(r'get_work_state/$', work.get_work_state),
    url(r'change_work_state/$', work.change_work_state),

    url(r'over_work/$', work.over_work),
    url(r'to_do_work/$', work.work_to_do),
    url(r'to_do/$', work.work_to_do_list),
    url(r'turn_off/$', work.work_shutdown),

    url(r'get_over_work/$', work.get_over_work),
    url(r'get_work_msg/$', work.get_work_msg),
    url(r'submit_work_msg/$', work.submit_work_msg),

    url(r'work_doing_list/$', work.work_doing),


]
