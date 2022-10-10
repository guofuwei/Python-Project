from django.db import models
from django.db.models.base import Model

# Create your models here.

class UserProfile(models.Model):
    username=models.CharField(max_length=11,verbose_name='用户名',unique=True,primary_key=True)
    nickname=models.CharField(max_length=30,verbose_name='昵称')
    email=models.EmailField(verbose_name='邮箱')
    phone=models.CharField(max_length=11,verbose_name='手机号')
    password=models.CharField(max_length=32,verbose_name='密码')
    sign=models.CharField(max_length=50,verbose_name='个人签名')
    info=models.CharField(max_length=150,verbose_name='个人描述')
    avatar=models.ImageField(upload_to='avatar',verbose_name='头像')
    created_time=models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    updated_time=models.DateTimeField(auto_now=True,verbose_name='更新时间')
