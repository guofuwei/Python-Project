'''
Author: hanshan-macbookair 2625406970@qq.com
Date: 2022-10-10 20:00:29
LastEditors: hanshan-macbookair 2625406970@qq.com
LastEditTime: 2022-10-21 15:13:25
FilePath: /Python-Project/backend/myblog/urls.py
Description: 整个项目的总体路由

Copyright (c) 2022 by hanshan-macbookair 2625406970@qq.com, All Rights Reserved. 
'''

from django.contrib import admin
from django.urls import path, include
from mytoken import views as token_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),  # 保留后台
    path('v1/users', include('user.urls')),  # 用户路由
    path('v1/tokens', token_views.login_view),  # 令牌路由
    path('v1/topics', include('topic.urls')),  # 文章路由
    path('v1/messages', include('message.urls')),  # 评论路由
]

# 设置静态文件路由
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
