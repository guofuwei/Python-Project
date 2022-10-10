from django.conf import settings
from django.http.response import JsonResponse
import jwt
from user.models import *


def login_check_dec(func):
    def wrap(request,*args,**kwargs):
        token=request.META.get('HTTP_AUTHORIZATION')
        if not token:
            return JsonResponse({'code':10104,'error':'未登录，请先登录'})
        try:
            dic=jwt.decode(token,key=settings.JWT_KEY)
        except Exception as ret:
            print(ret)
            return JsonResponse({'code':10104,'error':'未登录，请先登录'})
        username=dic['username']
        # print(username)
        try:
            user=UserProfile.objects.get(username=username)
            request.myuser=user
        except:
            return JsonResponse({'code':10105,'error':'非法请求'})
        return func(request,*args,**kwargs)
    return wrap

def is_blog_self_dec(func):
    def wrap(request,*args,**kwargs):
        token=request.META.get('HTTP_AUTHORIZATION')
        try:
            if jwt.decode(token,settings.JWT_KEY).get('username'):
                request.myusername=jwt.decode(token,settings.JWT_KEY).get('username')
            else:
                request.myusername=''
        except:
            request.myusername=''
        return func(request,*args,**kwargs)
    return wrap