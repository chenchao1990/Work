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

# mail_host = "smtp.163.com"       # 邮件服务器
# mail_user = "13716875340@163.com"
# user_email = "13716875340@163.com"
# user_pwd = "pwd1234"

# mail_host = "smtp.126.com"       # 邮件服务器
# mail_user = "spinache2do@126.com"
# user_email = "spinache2do@126.com"
# user_pwd = "pwd1234"

mail_host = "smtp.163.com"       # 邮件服务器
mail_user = "spinache2do@163.com"
user_email = "spinache2do@163.com"
user_pwd = "PWD1234"

# mail_host = "mail.gomeplus.com"       # 邮件服务器
# user_email = "chenchao-ds@gomeplus.com"
# mail_user = "chenchao-ds"
# user_pwd = "pwd@12345"
'''
# mail_host = "mail.gomeplus.com"       # 邮件服务器
mail_host = "10.58.45.230"       # 邮件服务器

user_email = "chenchao-ds@gomeplus.com"
mail_user = "chenchao-ds"
user_pwd = "pwd@12345"
'''


def send_email_to_idc(from_user, receive_list, msg_obj):
    file_obj = open('/opt/Sa_dir/myobj/work_log/send_mail.log', 'a+')
    try:
        server = smtplib.SMTP()                 # 创建发送对象
        server.connect(mail_host)               # 连接邮件服务器
        server.login(mail_user, user_pwd)  # 用户名和密码
        print "login successful"
        server.sendmail(from_user, receive_list, msg_obj.as_string())     # 发送邮件
        server.quit()
        file_obj.write("%s mail send successful \n" % mail_user)
        print 'mail_send successful!!!'
        return "success"
    except Exception, e:
        file_obj.write("%s mail ERROR: %s \n" % (mail_user, str(e)))
        print str(e)
        return "failed"
    finally:
        file_obj.close()


@app.task
def send_mail(title, email_msg, recive_email):
    # 创建一个带附件的实例
    msg_obj = MIMEMultipart()

    text_msg = MIMEText(email_msg, _subtype='plain', _charset='utf-8')
    msg_obj.attach(text_msg)
    receive_list = [recive_email, "SA@gomeplus.com"]          # 接受者
    # receive_list = ['465234371@qq.com', "chenchao-ds@gomeplus.com"]          # 接受者

    msg_obj['To'] = ";".join(receive_list)
    msg_obj['from'] = user_email                        # 发送者
    msg_obj['subject'] = '%s' % title         # 主题
    ret = send_email_to_idc(msg_obj['from'], receive_list, msg_obj)
    return ret



