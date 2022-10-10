from django.db import models
from topic.models import Topic
from user.models import UserProfile

# Create your models here.
class Message(models.Model):
    content=models.CharField(max_length=50,verbose_name='留言内容')
    created_time=models.DateTimeField(auto_now_add=True,verbose_name='留言创建时间')
    parent_message=models.IntegerField(verbose_name='父留言ID')
    publisher=models.ForeignKey(UserProfile,verbose_name='发布者',on_delete=models.CASCADE)
    topic=models.ForeignKey(Topic,verbose_name='文章',on_delete=models.CASCADE)
