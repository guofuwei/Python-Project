'''
Author: hanshan-server 2625406970@qq.com
Date: 2022-10-10 12:58:14
LastEditors: hanshan-server 2625406970@qq.com
LastEditTime: 2022-10-21 05:15:29
FilePath: /Python-Project/backend/tools/cache_tool.py
Description: 缓存工具

Copyright (c) 2022 by hanshan-server 2625406970@qq.com, All Rights Reserved. 
'''


from django.core.cache import cache


def cache_dec(expire):
    """装饰器，将数据库查出来的文章进行缓存

    Args:
        expire (int): 文章过期时间
    """
    def _cache_dec(func):
        def wrap(request, username, *args, **kwargs):
            # 只做详情页的缓存
            t_id = request.GET.get('t_id')
            if t_id:
                return func(request, username, *args, **kwargs)
            # 下面为详情页
            myusername = request.myusername
            if myusername == username:
                cache_key = 'cache_key_self_%s' % request.get_full_path()
            else:
                cache_key = 'cache_key_noself_%s' % request.get_full_path()
            # 如果当前缓存有这个文章
            if cache.get(cache_key):
                print('-----cache in-----')
                # 直接从缓存中返回数据
                return cache.get(cache_key)
            # 否则，从数据库中查取数据，并进行缓存
            else:
                print('=====view in=====')
                cache.set(cache_key, func(
                    request, username, *args, **kwargs), expire)
                return func(request, username, *args, **kwargs)
        return wrap
    return _cache_dec
