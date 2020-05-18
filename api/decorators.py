from functools import wraps

import coreschema

from api.docs import APISchema
from api.models import User
from api.response import AESJsonResponse
from vpo_admin.common import RedisUtil
from api import cache


def sign_exempt(view_func):
    """
    排除sign校验
    :return:
    """

    def wrapped_view(*args, **kwargs):
        return view_func(*args, **kwargs)

    wrapped_view.sign_exempt = True
    return wraps(view_func)(wrapped_view)


def jwt_exempt(view_func):
    """
    排除jwt_exempt校验
    :return:
    """

    def wrapped_view(*args, **kwargs):
        return view_func(*args, **kwargs)

    wrapped_view.jwt_exempt = True
    return wraps(view_func)(wrapped_view)


def rate_limit(rate):
    """
    :param rate 1/s,1/m,1/h
    接口限流
    :return:
    """

    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            user = request.user
            path = request.path_info
            method = request.method
            num, time = rate.split('/')
            len_time = len(time)
            unit = 1
            seconds = 0
            if len(time) > 1:
                unit = int(time[0:len_time - 1])
                time = time[-1]
            assert time in ['s', 'm', 'h']
            if time == 's':
                seconds = unit
            elif time == 'm':
                seconds = unit * 60
            elif time == 'h':
                seconds = unit * 3600
            conn = RedisUtil.conn
            cache_key = f'{cache.RATE_LIMIT_KEYS.format(path=path, method=method, user_id=user.pk)}'
            ret = int(conn.incr(cache_key))
            if ret == 1:
                conn.expire(cache_key, seconds)
            if int(ret) > int(num):
                return AESJsonResponse(status=403, msg='你的手速过快了，请稍后在试。')
            return func(request, *args, **kwargs)

        return inner

    return decorator
