'''
Author: hanshan-macbookair 2625406970@qq.com
Date: 2022-10-10 20:00:29
LastEditors: hanshan-macbookair 2625406970@qq.com
LastEditTime: 2022-10-21 15:21:24
FilePath: /Python-Project/backend/message/views.py
Description: 留言路由的具体处理逻辑

Copyright (c) 2022 by hanshan-macbookair 2625406970@qq.com, All Rights Reserved. 
'''
from django.http.response import JsonResponse
from django.shortcuts import render
import json
from message.models import Message
from tools.login_check import login_check_dec


@login_check_dec
def message_view(request, topic_id):
    """留言的具体生成逻辑

    Args:
        request (http request): 请求
        topic_id (int): 留言所属的文章id

    Returns:
        json: JsonResponse
    """
    if request.method != 'POST':
        return JsonResponse({'code': 10113, 'error': '非法请求'})
    json_str = request.body
    json_obj = json.loads(json_str)
    content = json_obj.get('content')
    parent_id = json_obj.get('parent_id', 0)
    myuser = request.myuser
    if not content:
        return JsonResponse({'code': 10114, 'error': '某些字段为空'})
    # 生成对应文章的留言
    Message.objects.create(content=content, parent_message=parent_id,
                           publisher=myuser, topic_id=topic_id)
    return JsonResponse({'code': 200})
