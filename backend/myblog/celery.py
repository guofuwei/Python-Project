'''
Author: hanshan-macbookair 2625406970@qq.com
Date: 2022-10-10 20:00:29
LastEditors: hanshan-macbookair 2625406970@qq.com
LastEditTime: 2022-10-21 15:21:43
FilePath: /Python-Project/backend/myblog/celery.py
Description: celery设置

Copyright (c) 2022 by hanshan-macbookair 2625406970@qq.com, All Rights Reserved. 
'''

from celery import Celery
from django.conf import settings
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myblog.settings')

app = Celery('myblog')
app.conf.update(
    BROKER_URL='redis://:123456@127.0.0.1:6379/1'
)

app.autodiscover_tasks(settings.INSTALLED_APPS)
