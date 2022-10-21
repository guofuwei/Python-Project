'''
Author: hanshan-server 2625406970@qq.com
Date: 2022-10-10 12:58:14
LastEditors: hanshan-server 2625406970@qq.com
LastEditTime: 2022-10-20 13:16:18
FilePath: /Python-Project/backend/user/tasks.py
Description: 定义celery的任务

Copyright (c) 2022 by hanshan-server 2625406970@qq.com, All Rights Reserved. 
'''


from myblog.celery import app
from tools.sms import Yuntongxin


@app.task
def sendsms_celery(phone, code):
    """celery发送短信

    Args:
        phone (string): 手机号
        code (string): 待发送的验证码
    """
    yuntongxin = Yuntongxin()
    yuntongxin.run(phone, code)
