'''
Author: hanshan-server 2625406970@qq.com
Date: 2022-10-14 09:06:06
LastEditors: hanshan-server 2625406970@qq.com
LastEditTime: 2022-10-20 13:20:34
FilePath: /Python-Project/backend/user/urls.py
Description: 与用户操作有关的路由表

Copyright (c) 2022 by hanshan-server 2625406970@qq.com, All Rights Reserved. 
'''

from django.urls import path
from . import views

urlpatterns = [
    path('/sms', views.sendSMS_view),  # 发送短信
    path('/emailcode', views.sendmail_view),  # 发送邮件
    path('/forgetpwd', views.forget_password_view),  # 忘记密码
    path('/<str:username>/avatar', views.update_avatar_view),  # 更新头像
    path('/<str:username>/password', views.update_password_view),  # 更新密码
    path('/<str:username>', views.UserView.as_view()),  # user的post，get等操作
    path('', views.UserView.as_view()),  # 获取用户信息
]
