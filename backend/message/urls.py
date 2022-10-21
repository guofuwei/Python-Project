'''
Author: hanshan-macbookair 2625406970@qq.com
Date: 2022-10-10 20:00:29
LastEditors: hanshan-macbookair 2625406970@qq.com
LastEditTime: 2022-10-21 15:18:23
FilePath: /Python-Project/backend/message/urls.py
Description: 留言的路由表

Copyright (c) 2022 by hanshan-macbookair 2625406970@qq.com, All Rights Reserved. 
'''

from django.urls import path
from . import views

urlpatterns = [
    path('/<int:topic_id>', views.message_view),
]
