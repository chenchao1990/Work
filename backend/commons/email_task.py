#!/usr/bin/env python
# _*_coding:utf-8 _*_

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from multiprocessing import Process, Pool
import commands
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

# mail_host = "smtp.163.com"       # 邮件服务器
# mail_user = "spinache2do@163.com"
# user_email = "spinache2do@163.com"
# user_pwd = "gomeplus123"

mail_host = "smtp.126.com"       # 邮件服务器
mail_user = "spinache2do@126.com"
user_email = "spinache2do@126.com"
user_pwd = "pwd1234"

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


def send_mail_by_thread(data_dict, recive_email):
    # 创建一个带附件的实例
    msg_obj = MIMEMultipart()

    # 构造邮件的文本内容
    email_msg = ""
    for key, value in data_dict.items():
        msg_ = key + ":" + str(value) + "\n"
        email_msg += msg_
    text_msg = MIMEText(email_msg, _subtype='plain', _charset='utf-8')
    msg_obj.attach(text_msg)
    receive_list = [recive_email, "SA@gomeplus.com"]                        # 接受者
    # receive_list = ['465234371@qq.com']                                   # 接受者

    msg_obj['To'] = ";".join(receive_list)
    msg_obj['from'] = mail_user                         # 发送者
    msg_obj['subject'] = '%s' % data_dict.pop('work_title')         # 主题

    pool = Pool(1)
    pool.apply_async(func=send_email_to_idc, args=(msg_obj['from'], receive_list, msg_obj,))

    print 'end'
    pool.close()
    # pool.teminate()  # 结束工作进程，不在处理未完成的任务。
    pool.join()     # 进程池中进程执行完毕后再关闭，如果注释，那么程序直接关闭。

