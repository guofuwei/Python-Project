'''
Author: hanshan-server 2625406970@qq.com
Date: 2022-10-10 12:58:14
LastEditors: hanshan-server 2625406970@qq.com
LastEditTime: 2022-10-21 05:01:30
FilePath: /Python-Project/backend/topic/urls.py
Description: 有关文章操作的路由

Copyright (c) 2022 by hanshan-server 2625406970@qq.com, All Rights Reserved. 
'''


from django.urls import path
from . import views

urlpatterns = [
    path('/<str:username>', views.blog_topic_view.as_view()),
]
