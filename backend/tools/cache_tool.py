from django.core.cache import cache


def cache_dec(expire):
    def _cache_dec(func):
        def wrap(request,username,*args,**kwargs):
            # 只做详情页的缓存
            t_id=request.GET.get('t_id')
            if t_id:
                return func(request,username,*args,**kwargs)
            # 下面为详情页
            myusername=request.myusername
            if myusername==username:
                cache_key='cache_key_self_%s' %request.get_full_path()
            else:
                cache_key='cache_key_noself_%s' %request.get_full_path()
            if cache.get(cache_key):
                print('-----cache in-----')
                return cache.get(cache_key)
            else:
                print('=====view in=====')
                cache.set(cache_key,func(request,username,*args,**kwargs),expire)
                return func(request,username,*args,**kwargs)
        return wrap
    return _cache_dec