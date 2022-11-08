'''
Author: hanshan-macbookair 2625406970@qq.com
Date: 2022-10-11 12:24:13
LastEditors: hanshan-macbookair 2625406970@qq.com
LastEditTime: 2022-11-08 15:30:25
FilePath: /Python-Project/backend/mytoken/views.py
Description: 登陆并生成登陆令牌

Copyright (c) 2022 by hanshan-macbookair 2625406970@qq.com, All Rights Reserved. 
'''

from django.http.response import JsonResponse
from django.shortcuts import render
import json
from user.models import *
import jwt
import hashlib
import time
from django.conf import settings


def login_view(request):
    """处理登陆事件的逻辑
    Args:
        request (http request):  请求

    Returns:
        json: JsonResponse
    """
    if not request.method == 'POST':
        return JsonResponse({'code': 10101, 'error': '非法请求'})
    json_str = request.body
    print(json_str)
    json_obj = json.loads(json_str)
    username = json_obj.get('username')
    password = json_obj.get('password')
    # 检查参数
    if not username or not password:
        return JsonResponse({'code': 10102, 'error': '用户名或密码为空!'})

    # 尝试查询该用户
    p = hashlib.md5()
    p.update(password.encode('utf-8'))
    password_m = p.hexdigest()
    try:
        UserProfile.objects.get(username=username, password=password_m)
    except Exception as ret:
        return JsonResponse({'code': 10103, 'error': '用户名或密码错误'})

    # 记录token会话状态保持
    result = {'code': 200, 'username': username,
              'data': {'token': make_token(username)}}
    return JsonResponse(result)


def make_token(username, expire=settings.JWT_EXPIRE):
    """利用jwt制作登陆令牌(token)

    Args:
        username (string): 用户名
        expire (int, optional): 令牌过期时间

    Returns:
        bytes: 制作好的令牌
    """
    key = settings.JWT_KEY
    payload = {'username': username, 'exp': time.time()+expire}
    return jwt.encode(payload=payload, key=key, algorithm='HS256').decode()
