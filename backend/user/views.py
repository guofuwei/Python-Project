from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse
from .models import *
import hashlib
from tools import sms 
import random
from django.core.cache import cache
from django.utils.decorators import method_decorator
from tools.login_check import login_check_dec
from .tasks import *

# Create your views here.
default_sign='这个人很懒，什么也没写'
default_info='这个人很懒，什么也没写'

@login_check_dec
def update_avatar_view(request,username):
    if request.method!='POST':
        return JsonResponse({'code':10109,'error':'非法请求'})
    avatar=request.FILES.get('avatar')
    myuser=request.myuser
    myuser.avatar=avatar
    myuser.save()
    return JsonResponse({'code':200,'error':''})



def sendSMS_view(request):
    #获取手机号和生成验证码
    code=random.randint(100000,999999)
    json_str=request.body
    json_obj=json.loads(json_str)
    phone=json_obj.get('phone')

    # 储存验证码
    cache_key='sms_%s' %phone
    old_key=cache.get(cache_key)
    if old_key:
        return JsonResponse({'code':10100,'error':'短信业务繁忙，请稍后再试'})
    cache.set(cache_key,code,180)

    # 发送验证码
    # sendsms(phone,code)
    sendsms_celery.delay(phone,code)

    return JsonResponse({'code':200})
def sendsms(phone,code):
    yuntongxin=sms.Yuntongxin()
    ret=yuntongxin.run(phone,code)

class UserView(View):
    # v1/users/<username>
    def post(self,request):
        json_string=request.body
        json_obj=json.loads(json_string)
        username=json_obj.get('username')
        email=json_obj.get('email')
        phone=json_obj.get('phone')
        sms_num=json_obj.get('sms_num')
        password1=json_obj.get('password_1')
        password2=json_obj.get('password_2')

        # 参数检查
        if not json_string:
            return JsonResponse({'code':202,'error':'请求中无内容'})
        cache_key='sms_%s' %phone
        if not cache.get(cache_key):
            return JsonResponse({'code':201,'error':'验证码已过期'})
        if not cache.get(cache_key)==int(sms_num):
            print(cache.get(cache_key))
            print(sms_num)
            return JsonResponse({'code':208,'error':'验证码不正确'})
        if not username:
            return JsonResponse({'code':203,'error':'请求中未提交用户名'})
        if not email:
            return JsonResponse({'code':204,'error':'请求中未提交邮箱'})
        if not password1 or not password2:
            return JsonResponse({'code':205,'error':'请求中未提交密码'})
        if password1!=password2:
            return JsonResponse({'code':206,'error':'两次提交的密码不一致'})
        try:
            UserProfile.objects.get(username=username)
            return JsonResponse({'code':207,'error':'用户名已存在'})
        except:
            pass

        # 对密码进行加密
        p_m=hashlib.md5()
        p_m.update(password1.encode('utf-8'))
        password=p_m.hexdigest()

        UserProfile.objects.create(username=username,nickname=username,email=email
        ,phone=phone,password=password,sign=default_sign,info=default_info)
        
        return JsonResponse({'code':200,'username':username,'data':''})


    @method_decorator(login_check_dec)
    def get(self,request,username):
        # 校验参数
        # print(request)
        myuser=request.myuser
        try:
            theuser=UserProfile.objects.get(username=username)
        except Exception as ret:
            return JsonResponse({'code':10106,'error':'非法请求'})
        if not theuser==myuser:
            return JsonResponse({'code':10106,'error':'非法请求'})

        # 返回数据 
        data={
            'info':theuser.info,
            'sign':theuser.sign,
            'nickname':theuser.nickname,
            'avatar':str(theuser.avatar),
        }
        return JsonResponse({'code':200,'username':theuser.username,'data':data})


    @method_decorator(login_check_dec)
    def put(self,request,username):
        # 校验参数
        if not username:
            return JsonResponse({'code':10107,'error':'非法请求'})
        try:
            theuser=UserProfile.objects.get(username=username)
        except Exception as ret:
            return JsonResponse({'code':10108,'error':'该用户不存在'})
        if theuser!=request.myuser:
            return JsonResponse({'code':10107,'error':'非法请求'})
        # 拿取参数并更新
        json_str=request.body
        json_obj=json.loads(json_str)
        theuser.sign=json_obj.get('sign')
        theuser.info=json_obj.get('info')
        theuser.nickname=json_obj.get('nickname')
        theuser.save()
        return JsonResponse({'code':200,'username':username})

    


