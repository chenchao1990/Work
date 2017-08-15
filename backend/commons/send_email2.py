#!/usr/bin/env python
# _*_coding:utf-8 _*_

from multiprocessing import Process, Pool
import commands
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib


class Mail(object):
    def __init__(self):
        self.mail_host = "mail.yolo24.com"
        self.mail_user = "chenchao-ds"
        self.mail_pass = "pwd@12345"
        self.user_email = "chenchao-ds@yolo24.com"

    def send_email_to_idc(self, from_user, receive_list, msg_obj):
        try:
            server = smtplib.SMTP()                 # 创建发送对象
            server.connect(self.mail_host)               # 连接邮件服务器
            server.login(self.mail_user, self.mail_pass)  # 用户名和密码
            print "login successful"
            # server.sendmail(msg['from'], msg['to'],msg.as_string())
            server.sendmail(from_user, receive_list, msg_obj.as_string())     # 发送邮件
            server.quit()
            print 'mail_send success!!!!!!!!!!!!!!!!!!!'
        except Exception, e:
            print str(e)

    def send_mail_by_thread(self, data_dict):
        # 创建一个带附件的实例
        msg_obj = MIMEMultipart()

        # 构造邮件的文本内容
        email_msg = ""
        i = 0
        print "all data count ", len(data_dict.keys())
        for key, value in data_dict.items():
            i+=1
            print "iiiiiiiiiiii", i
            msg_ = key + ":" + str(value) + "\n"
            email_msg += msg_
        text_msg = MIMEText(email_msg, _subtype='plain', _charset='utf-8')
        msg_obj.attach(text_msg)

        receive_list = ['chenchao-ds@yolo24.com']       # 接收人列表
        # 发送邮件
        # 加邮件头
        # msg['to'] = 'wangyan@yolo24.com'                        # 接收者
        msg_obj['To'] = ";".join(receive_list)
        msg_obj['from'] = self.user_email                              # 发送者
        msg_obj['subject'] = '%s' % data_dict.pop('title')        # 主 题

        pool = Pool(1)
        pool.apply_async(func=self.send_email_to_idc, args=(self.user_email, receive_list, msg_obj,))

        print 'end'
        pool.close()
        # pool.teminate()  # 结束工作进程，不在处理未完成的任务。
        pool.join()     # 进程池中进程执行完毕后再关闭，如果注释，那么程序直接关闭。
