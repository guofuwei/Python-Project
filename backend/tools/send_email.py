'''
Author: hanshan-server 2625406970@qq.com
Date: 2022-10-14 09:06:06
LastEditors: hanshan-server 2625406970@qq.com
LastEditTime: 2022-10-21 05:20:56
FilePath: /Python-Project/backend/tools/send_email.py
Description: 发送邮件验证码工具

Copyright (c) 2022 by hanshan-server 2625406970@qq.com, All Rights Reserved. 
'''

from django.core.mail import send_mail
import random


def send_email(code, recv_mail):
    """发送邮件验证码

    Args:
        code (string): 验证码
        recv_mail (string): 接受验证码的邮箱
    """
    send_mail(
        subject='邮件验证码',
        message='您的验证码是'+str(code)+",该验证码3分钟内有效",
        from_email='3555970235@qq.com',
        recipient_list=[recv_mail],
        fail_silently=False
    )
