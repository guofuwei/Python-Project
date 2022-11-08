'''
Author: hanshan-server 2625406970@qq.com
Date: 2022-10-14 09:06:51
LastEditors: hanshan-macbookair 2625406970@qq.com
LastEditTime: 2022-11-08 15:32:34
FilePath: /Python-Project/backend/user/views.py
Description: 用户的有关处理逻辑

Copyright (c) 2022 by hanshan-server 2625406970@qq.com, All Rights Reserved. 
'''

import email
from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse
from pydantic import ConstrainedFloat, Json
from .models import *
import hashlib
from tools import sms
import random
from django.core.cache import cache
from django.utils.decorators import method_decorator
from tools.login_check import login_check_dec
from tools.send_email import send_email
from .tasks import *

default_sign = '这个人很懒，什么也没写'  # 默认用户签名
default_info = '这个人很懒，什么也没写'  # 默认用户简介


@login_check_dec
def update_avatar_view(request, username):
    """更新头像

    Args:
        request (http request): 请求
        username (string): 用户名

    Returns:
        json: 以json格式返回
    """
    # 排除非法请求
    if request.method != 'POST':
        return JsonResponse({'code': 10109, 'error': '非法请求'})
    avatar = request.FILES.get('avatar')  # 获取头像
    myuser = request.myuser
    myuser.avatar = avatar
    myuser.save()  # 保存头像
    return JsonResponse({'code': 200, 'error': ''})


@login_check_dec
def update_password_view(request, username):
    """更新密码

    Args:
        request (http request): 请求
        username (string): 用户名

    Returns:
        json: 以json格式返回
    """
    if request.method != 'POST':
        return JsonResponse({'code': 10109, 'error': '非法请求'})
    myuser = request.myuser
    json_str = request.body
    json_obj = json.loads(json_str)  # 拿取request body
    password_new = json_obj.get('password_new')
    password_new2 = json_obj.get('password_new2')
    if not password_new or not password_new2:
        return JsonResponse({'code': 10101, 'error': '新密码不能为空'})
     # 对密码进行加密
    p_m = hashlib.md5()
    p_m.update(password_new.encode('utf-8'))
    password = p_m.hexdigest()
    myuser.password = password
    myuser.save()  # 保存新密码
    return JsonResponse({'code': 200, 'error': ''})


def forget_password_view(request):
    """忘记密码

    Args:
        request (http request): 请求

    Returns:
        json: 以json格式返回
    """
    if request.method != 'POST':
        return JsonResponse({'code': 10109, 'error': '非法请求'})
    json_str = request.body
    json_obj = json.loads(json_str)
    if not json_str:
        return JsonResponse({'code': 202, 'error': '请求中无内容'})
    # 拿取request body中的各种参数
    email = json_obj.get('email')
    email_code = json_obj.get('email_code')
    password_new = json_obj.get('password_new1')
    password_new2 = json_obj.get('password_new2')
    # 拿取缓存中的邮件验证码
    cache_key = 'email_code_%s' % email
    cache_code = cache.get(cache_key)
    try:
        int_email = int(email_code)
    except:
        return JsonResponse({'code': 208, 'error': '验证码不正确'})
    if not cache_code:
        return JsonResponse({'code': 201, 'error': '验证码已过期'})
    if not cache_code == int_email:
        return JsonResponse({'code': 208, 'error': '验证码不正确'})
    if not password_new or not password_new2:
        return JsonResponse({'code': 10101, 'error': '新密码不能为空'})
    if password_new != password_new2:
        return JsonResponse({'code': 206, 'error': '两次提交的密码不一致'})
    try:
        user = UserProfile.objects.get(email=email)
    except:
        return JsonResponse({'code': 207, 'error': '该用户不存在'})
    # 对密码进行加密
    p_m = hashlib.md5()
    p_m.update(password_new.encode('utf-8'))
    password = p_m.hexdigest()
    # 保存新密码
    user.password = password
    # 保存密码
    user.save()
    return JsonResponse({'code': 200, 'error': ''})


def sendmail_view(request):
    # 获取手机号和生成验证码
    code = random.randint(100000, 999999)
    json_str = request.body
    json_obj = json.loads(json_str)
    email = json_obj.get('email')

    if not email:
        return JsonResponse({'code': 10101, 'error': '邮箱不能为空'})

    # 储存验证码
    cache_key = 'email_code_%s' % email
    # old_key = cache.get(cache_key)
    # if old_key:
    #     return JsonResponse({'code': 10100, 'error': '邮件已发送，请勿重复点击'})
    cache.set(cache_key, code, 180)

    # 发送验证码
    send_email(code, email)

    return JsonResponse({'code': 200})


class UserView(View):
    """关于用户的post,get,put的操作
    """

    def post(self, request):
        """注册请求

        Args:
            request (http request): 请求

        Returns:
            json: 以json格式返回
        """
        json_string = request.body
        json_obj = json.loads(json_string)
        username = json_obj.get('username')
        email = json_obj.get('email')
        email_code = json_obj.get('email_code')
        password1 = json_obj.get('password')
        password2 = json_obj.get('password2')

        # 参数检查
        cache_key = 'email_code_%s' % email
        cache_code = cache.get(cache_key)
        try:
            int_email = int(email_code)
        except:
            return JsonResponse({'code': 208, 'error': '验证码不正确'})
        if not json_string:
            return JsonResponse({'code': 202, 'error': '请求中无内容'})
        if not cache_code:
            return JsonResponse({'code': 201, 'error': '验证码已过期'})
        if not cache_code == int_email:
            # print(cache.get(cache_key))
            # print(int_email)
            return JsonResponse({'code': 208, 'error': '验证码不正确'})
        if not username:
            return JsonResponse({'code': 203, 'error': '请求中未提交用户名'})
        if not email:
            return JsonResponse({'code': 204, 'error': '请求中未提交邮箱'})
        if not password1 or not password2:
            return JsonResponse({'code': 205, 'error': '请求中未提交密码'})
        if password1 != password2:
            return JsonResponse({'code': 206, 'error': '两次提交的密码不一致'})
        try:
            UserProfile.objects.get(email=email)  # type: ignore
            return JsonResponse({'code': 207, 'error': '该邮箱已注册'})
        except:
            pass
        try:
            UserProfile.objects.get(username=username)
            return JsonResponse({'code': 207, 'error': '该账户已注册'})
        except:
            pass

        # 对密码进行加密
        p_m = hashlib.md5()
        p_m.update(password1.encode('utf-8'))
        password = p_m.hexdigest()

        # 新建用户
        UserProfile.objects.create(username=username, nickname=username, email=email,
                                   password=password, sign=default_sign, info=default_info)
        return JsonResponse({'code': 200, 'username': username, 'data': ''})

    @method_decorator(login_check_dec)
    def get(self, request, username):
        """获取用户信息请求

        Args:
            request (http request): 请求
            username (string): 用户名

        Returns:
            json: 以json格式返回
        """
        # 校验参数
        myuser = request.myuser
        try:
            theuser = UserProfile.objects.get(username=username)
        except Exception as ret:
            return JsonResponse({'code': 10106, 'error': '非法请求'})
        if not theuser == myuser:
            return JsonResponse({'code': 10106, 'error': '非法请求'})

        # 返回数据
        data = {
            'info': theuser.info,
            'sign': theuser.sign,
            'nickname': theuser.nickname,
            'avatar': str(theuser.avatar),
        }
        return JsonResponse({'code': 200, 'username': theuser.username, 'data': data})

    @method_decorator(login_check_dec)
    def put(self, request, username):
        """获取用户信息请求

        Args:
            request (http request): 请求
            username (string): 用户名

        Returns:
            json: 以json格式返回
        """
        # 校验参数
        if not username:
            return JsonResponse({'code': 10107, 'error': '非法请求'})
        try:
            theuser = UserProfile.objects.get(username=username)
        except Exception as ret:
            return JsonResponse({'code': 10108, 'error': '该用户不存在'})
        if theuser != request.myuser:
            return JsonResponse({'code': 10107, 'error': '非法请求'})
        # 拿取参数并更新
        json_str = request.body
        json_obj = json.loads(json_str)
        theuser.sign = json_obj.get('sign')
        theuser.info = json_obj.get('info')
        theuser.nickname = json_obj.get('nickname')
        theuser.save()
        return JsonResponse({'code': 200, 'username': username})
