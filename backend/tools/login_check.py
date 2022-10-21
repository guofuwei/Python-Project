'''
Author: hanshan-server 2625406970@qq.com
Date: 2022-10-10 12:58:14
LastEditors: hanshan-server 2625406970@qq.com
LastEditTime: 2022-10-21 05:19:30
FilePath: /Python-Project/backend/tools/login_check.py
Description: 登陆检查工具

Copyright (c) 2022 by hanshan-server 2625406970@qq.com, All Rights Reserved. 
'''

from django.conf import settings
from django.http.response import JsonResponse
import jwt
from user.models import *


def login_check_dec(func):
    """登陆检查装饰器
    """
    def wrap(request, *args, **kwargs):
        """对请求进行登陆检查
        """
        # 拿取token
        token = request.META.get('HTTP_AUTHORIZATION')
        if not token:
            return JsonResponse({'code': 10104, 'error': '未登录，请先登录'})
        try:
            dic = jwt.decode(token, key=settings.JWT_KEY)
        except Exception as ret:
            print(ret)
            return JsonResponse({'code': 10104, 'error': '未登录，请先登录'})
        username = dic['username']
        # print(username)
        try:
            # 将当前用户的数据存在request.myuser
            user = UserProfile.objects.get(username=username)
            request.myuser = user
        except:
            return JsonResponse({'code': 10105, 'error': '非法请求'})
        return func(request, *args, **kwargs)
    return wrap


def is_blog_self_dec(func):
    """装饰器，文章作者是否是当前登陆用户的检查
    """
    def wrap(request, *args, **kwargs):
        """文章作者是否是当前登陆用户的检查
        """
        # 拿取token
        token = request.META.get('HTTP_AUTHORIZATION')
        try:
            if jwt.decode(token, settings.JWT_KEY).get('username'):
                request.myusername = jwt.decode(
                    token, settings.JWT_KEY).get('username')
            else:
                request.myusername = ''
        except:
            request.myusername = ''
        # print(request.myusername)
        return func(request, *args, **kwargs)
    return wrap
