from django.db import models
from django.db.models.fields import TextField
from user.models import UserProfile


# Create your models here.

class Topic(models.Model):
    title=models.CharField(max_length=50,verbose_name='文章标题')
    category=models.CharField(max_length=20,verbose_name='博客的分类')
    limit=models.CharField(max_length=10,verbose_name='权限')
    introduce=models.CharField(max_length=90,verbose_name='博客简介')
    content=models.TextField(verbose_name='博客内容')
    created_time=models.DateTimeField(auto_now_add=True,verbose_name='博客创建时间')
    updated_time=models.DateTimeField(auto_now=True,verbose_name='博客修改时间')
    author=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
