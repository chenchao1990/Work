#!/usr/bin/env python
# _*_coding:utf-8 _*_

from __future__ import absolute_import
from mail_send.celery import app
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib


mail_host = "smtp.163.com"       # 邮件服务器
mail_user = "spinache2do@163.com"
user_email = "spinache2do@163.com"
user_pwd = "gomeplus123"

'''
# mail_host = "mail.gomeplus.com"       # 邮件服务器
mail_host = "10.58.45.230"       # 邮件服务器

user_email = "chenchao-ds@gomeplus.com"
mail_user = "chenchao-ds"
user_pwd = "pwd@12345"
'''


def send_email_to_idc(from_user, receive_list, msg_obj):
    try:
        server = smtplib.SMTP()                 # 创建发送对象
        server.connect(mail_host)               # 连接邮件服务器
        server.login(mail_user, user_pwd)  # 用户名和密码
        print "login successful"
        # server.sendmail(msg['from'], msg['to'],msg.as_string())
        server.sendmail(from_user, receive_list, msg_obj.as_string())     # 发送邮件
        server.quit()
        print 'mail_send successful!!!'
    except Exception, e:
        print str(e)


@app.task
def send_mail(title, email_msg, recive_email):
    # 创建一个带附件的实例
    msg_obj = MIMEMultipart()

    # 构造邮件的文本内容
    # email_msg = ""
    # for key, value in data_dict.items():
    #     print key, value, type(key), type(value)
    #     msg_ = key + ":" + str(value) + "\n"
    #     email_msg += msg_
    text_msg = MIMEText(email_msg, _subtype='plain', _charset='utf-8')
    msg_obj.attach(text_msg)
    # receive_list = [recive_email, "SA@gomeplus.com"]                        # 接受者
    receive_list = ['465234371@qq.com']                                   # 接受者

    msg_obj['To'] = ";".join(receive_list)
    msg_obj['from'] = 'spinache2do@163.com'                         # 发送者
    msg_obj['subject'] = '%s' % title         # 主题

    send_email_to_idc(msg_obj['from'], receive_list, msg_obj)
    print 'end'


