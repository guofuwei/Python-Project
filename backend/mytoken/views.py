from django.http.response import JsonResponse
from django.shortcuts import render
import json
from user.models import *
import jwt
import hashlib
import time
from django.conf import settings


# Create your views here.
def login_view(request):
    if not request.method=='POST':
        return JsonResponse({'code':10101,'error':'非法请求'})
    json_str=request.body
    print(json_str)
    json_obj=json.loads(json_str)
    username=json_obj.get('username')
    password=json_obj.get('password')
    # print(username)
    # print(password)
    if not username or not password:
        return JsonResponse({'code':10102,'error':'用户名或密码为空!'})
    
    #尝试查询该用户
    p=hashlib.md5()
    p.update(password.encode('utf-8'))
    password_m=p.hexdigest()
    try:
        UserProfile.objects.get(username=username,password=password_m)
    except Exception as ret:
        return JsonResponse({'code':10103,'error':'用户名或密码错误'})

    # 记录token会话状态保持
    result={'code':200,'username':username,'data':{'token':make_token(username)}}
    return JsonResponse(result)

    
def make_token(username,expire=settings.JWT_EXPIRE):
    key=settings.JWT_KEY
    payload={'username':username,'exp':time.time()+expire}
    return jwt.encode(payload=payload,key=key,algorithm='HS256').decode()