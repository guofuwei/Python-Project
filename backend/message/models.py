'''
Author: hanshan-macbookair 2625406970@qq.com
Date: 2022-10-11 12:24:13
LastEditors: hanshan-macbookair 2625406970@qq.com
LastEditTime: 2022-10-21 15:17:28
FilePath: /Python-Project/backend/message/models.py
Description: 关于留言的sql表设计

Copyright (c) 2022 by hanshan-macbookair 2625406970@qq.com, All Rights Reserved. 
'''

from django.db import models
from topic.models import Topic
from user.models import UserProfile


class Message(models.Model):
    """留言设计字段表
    """
    content = models.CharField(max_length=50, verbose_name='留言内容')
    created_time = models.DateTimeField(
        auto_now_add=True, verbose_name='留言创建时间')
    parent_message = models.IntegerField(verbose_name='父留言ID')
    publisher = models.ForeignKey(
        UserProfile, verbose_name='发布者', on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, verbose_name='文章',
                              on_delete=models.CASCADE)
