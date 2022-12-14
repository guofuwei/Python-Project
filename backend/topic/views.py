'''
Author: hanshan-server 2625406970@qq.com
Date: 2022-10-10 12:58:14
LastEditors: hanshan-server 2625406970@qq.com
LastEditTime: 2022-10-21 05:11:30
FilePath: /Python-Project/backend/topic/views.py
Description: 有关文章操作的详细处理逻辑

Copyright (c) 2022 by hanshan-server 2625406970@qq.com, All Rights Reserved. 
'''

import json
from django.http.response import JsonResponse
from user.models import UserProfile
from django.shortcuts import render
from tools.login_check import is_blog_self_dec, login_check_dec
from tools.cache_tool import cache_dec
from topic.models import Topic
from django.utils.decorators import method_decorator
from django.views import View
from django.core.cache import cache
from time import strftime
from message.models import Message
from django.db.models import Q


class blog_topic_view(View):
    """有关文章的所有处理逻辑
    """

    def make_topic_res(self, author, author_topics):
        """生成多篇文章

        Args:
            author (string): 作者
            author_topics (string): 数据库查出来的文章

        Returns:
            json: json格式
        """
        topic_res = []
        for topic in author_topics:
            topic_res.append({
                'id': topic.id,
                'title': topic.title,
                'category': topic.category,
                'created_time': topic.created_time.strftime('%Y-%m-%d %H:%M:%S'),
                'introduce': topic.introduce,
                'author': topic.author_id,
            })
        return JsonResponse({
            'code': 200,
            'data': {
                'nickname': author.nickname,
                'topics': topic_res,
            }
        })

    def make_topic_detail_res(self, request, author, thetopic):
        """生成一篇文章的详细信息，包括留言

        Args:
            request (http request): 请求
            author (string): 作者
            thetopic (string): 数据库查处来的该篇文章

        Returns:
            json: json格式
        """
        # 生成上下一篇文章的id
        myusername = request.myusername
        if myusername == author.username:
            next_topic = Topic.objects.filter(
                id__gt=thetopic.id, author=author).first()
            last_topic = Topic.objects.filter(
                id__lt=thetopic.id, author=author).last()
        else:
            next_topic = Topic.objects.filter(
                id__gt=thetopic.id, limit='public', author=author).first()
            last_topic = Topic.objects.filter(
                id__lt=thetopic.id, limit='public', author=author).last()
        # 开始生成留言和回复
        # 准备工作
        msgs = Message.objects.filter(topic=thetopic)
        msg_list = []
        rep_dic = {}
        m_count = 0
        for msg in msgs:
            if msg.parent_message:
                rep_dic.setdefault(msg.parent_message, [])
                rep_dic[msg.parent_message].append({'msg_id': msg.id, 'content': msg.content,
                                                    'publisher': msg.publisher.nickname, 'publisher_avatar': str(msg.publisher.avatar),
                                                    'created_time': msg.created_time.strftime('%Y-%m-%d %H:%M:%S ')})
            else:
                m_count += 1
                msg_list.append({'id': msg.id, 'content': msg.content,
                                 'publisher': msg.publisher.nickname, 'publisher_avatar': str(msg.publisher.avatar),
                                 'created_time': msg.created_time.strftime('%Y-%m-%d %H:%M:%S '), 'reply': []})
        # 正式生成
        for msg in msg_list:
            if msg['id'] in rep_dic:
                msg['reply'] = rep_dic[msg['id']]

        # 返回数据
        data = {
            'nickname': author.nickname,
            'title': thetopic.title,
            'category': thetopic.category,
            'limit': thetopic.limit,
            'created_time': thetopic.created_time.strftime('%Y-%m-%d %H:%M:%S'),
            'content': thetopic.content,
            'introduce': thetopic.introduce,
            'author': author.username,
            'next_id': next_topic.id if next_topic else None,
            'next_title': next_topic.title if next_topic else '',
            'last_id': last_topic.id if last_topic else None,
            'last_title': last_topic.title if last_topic else '',
            'messages': msg_list,
            'messages_count': m_count,
        }
        return data

    def delete_cache(self, request):
        """删除文章的redis缓存
        """
        cache_key_header = ['cache_key_self_', 'cache_key_noself_']
        cache_key_tail = ['?category=tec', '?category=no-tec', '']
        cache_keys = list()
        for header in cache_key_header:
            for tail in cache_key_tail:
                cache_keys.append(header+tail)
        cache.delete_many(cache_keys)
        print('-----cache delete success-----')

    @method_decorator(is_blog_self_dec)
    @method_decorator(cache_dec(10))
    def get(self, request, username):
        """get请求,获取文章

        Args:
            request (http request): 请求
            username (string): 用户名

        Returns:
            json: json格式
        """
        # 尝试获取有无分类和具体哪篇文章的信息
        category = request.GET.get('category')
        t_id = request.GET.get('t_id')
        try:
            user = UserProfile.objects.get(username=username)
        except:
            return JsonResponse({'code': 200, 'error': '该用户不存在'})

        # 获取所有公开文章
        if not category and not t_id:
            # v1/<username>/topics
            topics = Topic.objects.filter(
                Q(limit="public") | Q(author_id=username))

            return self.make_topic_res(user, topics)

         # 按技术和非技术进行分类
        elif category:
            # v1/<username>/topics?category=tec/no-tec
            topics = Topic.objects.filter(
                Q(limit='public') | Q(author_id=username), category=category)
            return self.make_topic_res(user, topics)

        # 具体页面
        elif t_id:
            # /v1/<username>/topics?t_id=1
            try:
                thetopic = Topic.objects.get(author_id=username, id=t_id)
            except Exception as ret:
                return JsonResponse({'code': 10111, 'error': '该文章不存在'})
            data = self.make_topic_detail_res(request, user, thetopic)
            return JsonResponse({'code': 200, 'data': data})

    @method_decorator(is_blog_self_dec)
    def post(self, request, username):
        """post请求,发表文章

        Args:
            request (http request): 请求
            username (string): 用户名

        Returns:
            json: json格式
        """
        json_str = request.body
        json_obj = json.loads(json_str)
        # 'content': content, 'content_text':content_text,
        # 'limit': limit, 'title':title, 'category':category
        content = json_obj.get('content')
        content_text = json_obj.get('content_text')
        if content_text:
            introduce = content_text[:30]
        else:
            introduce = content[:30]
        limit = json_obj.get('limit')
        title = json_obj.get('title')
        category = json_obj.get('category')
        # 检查某些字段是否为空
        if not content or not limit or not title or not category:
            return JsonResponse({'code': 10111, 'error': '某些字段为空！'})

        myusername = request.myusername
        # 新建文章，存入数据库
        Topic.objects.create(content=content, limit=limit, title=title,
                             category=category, author_id=myusername, introduce=introduce)
        # 删除缓存
        self.delete_cache(request)
        return JsonResponse({'code': 200})

    @method_decorator(is_blog_self_dec)
    def put(self, request, username):
        """put请求,修改文章

        Args:
            request (http request): 请求
            username (string): 用户名

        Returns:
            json: json格式
        """
        json_str = request.body
        json_obj = json.loads(json_str)
        tid = json_obj.get('t_id')
        content = json_obj.get('content')
        content_text = json_obj.get('content_text')
        if content_text:
            introduce = content_text[:30]
        else:
            introduce = content[:30]
        limit = json_obj.get('limit')
        title = json_obj.get('title')
        category = json_obj.get('category')
        if not content or not limit or not title or not category or not tid:
            return JsonResponse({'code': 10111, 'error': '某些字段为空！'})

        myusername = request.myusername
        # 更新文章，存入数据库
        Topic.objects.filter(id=tid).update(content=content, limit=limit, title=title,
                                            category=category, author_id=myusername, introduce=introduce)
        # 删除缓存
        self.delete_cache(request)
        return JsonResponse({'code': 200})

    @method_decorator(is_blog_self_dec)
    def delete(self, request, username):
        """delete请求,删除文章

        Args:
            request (http request): 请求
            username (string): 用户名

        Returns:
            json: json格式
        """
        # /v1/<username>/topics?t_id=1
        t_id = request.GET.get('t_id')
        if username == request.myusername:
            try:
                # 在数据库中删除
                topic = Topic.objects.get(id=t_id)
                topic.delete()
                # 删除缓存
                self.delete_cache(request)
                return JsonResponse({'code': 200})
            except:
                return JsonResponse({'code': 10112, 'error': '非法请求'})
        else:
            return JsonResponse({'code': 10112, 'error': '非法请求'})
