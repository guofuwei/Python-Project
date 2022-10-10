from django.http.response import JsonResponse
from django.shortcuts import render
import json
from message.models import Message
from tools.login_check import login_check_dec

# Create your views here.

@login_check_dec
def message_view(request,topic_id):
    if request.method!='POST':
        return JsonResponse({'code':10113,'error':'非法请求'})
    json_str=request.body
    json_obj=json.loads(json_str)
    content=json_obj.get('content')
    parent_id=json_obj.get('parent_id',0)
    myuser=request.myuser
    if not content:
        return JsonResponse({'code':10114,'error':'某些字段为空'})
    Message.objects.create(content=content,parent_message=parent_id,
    publisher=myuser,topic_id=topic_id)
    return JsonResponse({'code':200})