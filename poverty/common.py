import base64
import datetime
import hashlib
import json
import random
import re
import string
import time

import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from django.conf import settings
from django.contrib.auth.password_validation import MinimumLengthValidator, NumericPasswordValidator
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils import timezone
from django_redis import get_redis_connection
from redis import Redis


class AESUtil:
    key = str.encode(settings.PRIVATE_KEY)

    def __init__(self, key=None):
        if key:
            self.key = str.encode(key)

    def encrypt_data(self, data):
        data = data.encode()
        aes = AES.new(self.key, AES.MODE_ECB)
        pad_data = pad(data, AES.block_size, style='pkcs7')
        return str(base64.encodebytes(aes.encrypt(pad_data)), encoding='utf8').replace('\n', '')

    def decrypt_data(self, data):
        aes = AES.new(self.key, AES.MODE_ECB)
        pad_data = pad(data, AES.block_size, style='pkcs7')
        return str(unpad(aes.decrypt(base64.decodebytes(pad_data)), block_size=AES.block_size).decode('utf8'))


def is_phone(phone):
    """
    验证号码是否符合格式
    :param phone: 电话号码
    :return:
    """
    if phone:
        reg = r'^[1][0-9]{10}$'
        p = re.compile(reg)
        return p.match(phone)
    return False


def md5_encode(s):
    """
    md5加密
    :param s:
    :return:
    """
    m = hashlib.md5(s.encode(encoding='utf-8'))
    return m.hexdigest()


def datetime_now(d=0, h=0, m=0, s=0):
    """
    取之前时间
    :param s: 秒
    :param d: 天
    :param h: 小时
    :param m: 分钟
    :return:
    """
    tmp = timezone.now()
    if d:
        tmp -= datetime.timedelta(days=d)
    if h:
        tmp -= datetime.timedelta(hours=h)
    if m:
        tmp -= datetime.timedelta(minutes=m)
    if s:
        tmp -= datetime.timedelta(seconds=s)
    return tmp


def validate_password(password):
    """
    校验密码强度
    :param password:
    :return:
    """
    try:
        MinimumLengthValidator(6).validate(password)
        # CommonPasswordValidator().validate(password)
        NumericPasswordValidator().validate(password)
        return True
    except ValidationError as e:
        return False


def generate_random_string(length, is_digits=False, exclude=None):
    """
    生成任意长度字符串
    :param exclude:
    :param is_digits:
    :param length:
    :return:
    """
    if is_digits:
        all_char = string.digits
    else:
        all_char = string.ascii_letters + string.digits
    if exclude:
        for char in exclude:
            all_char.replace(char, '')
    return ''.join(random.sample(all_char, length))


def dict_fetchall(cursor):
    """
    cursor返回dict
    :param cursor:
    :return:
    """
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


class RedisUtil:
    """
    封装缓存方法
    """
    conn = get_redis_connection('pers')  # type:Redis

    @classmethod
    def _exp_of_none(cls, *args, exp_of_none, callback):
        if not cls.conn.exists(args[0]):
            ret = callback(*args)
            if exp_of_none:
                cls.conn.expire(args[0], exp_of_none)
        else:
            ret = callback(*args)
        return ret

    @classmethod
    def get_or_set(cls, key, default=None, value_fun=None):
        """
        获取或者设置缓存
        :param key:
        :param default: 默认值，优先于value_fun
        :param value_fun: 默认取值函数
        :return:
        """
        value = cls.conn.get(key)
        if value is None and default:
            return default
        if value is not None:
            return value.decode()
        if value_fun:
            value, exp = value_fun()
            cls.conn.set(key, value, exp)
        return value

    @classmethod
    def get(cls, key, default=None):
        value = cls.conn.get(key)
        if value is None:
            return default
        return value.decode()

    @classmethod
    def set(cls, key, value, exp=None):
        """
        设置缓存
        :param key:
        :param value:
        :param exp:
        :return:
        """
        return cls.conn.set(key, value, exp)

    @classmethod
    def delete(cls, key):
        """
        缓存清除，接收list or str
        :param key:
        :return:
        """
        return cls.conn.delete(key)

    @classmethod
    def sadd(cls, name, values, exp_of_none=None):
        return cls._exp_of_none(name, values, exp_of_none=exp_of_none, callback=cls.conn.sadd)

    @classmethod
    def hset(cls, name, key, value, exp_of_none=None):
        return cls._exp_of_none(name, key, value, exp_of_none=exp_of_none, callback=cls.conn.hset)

    @classmethod
    def hincrby(cls, name, key, value=1, exp_of_none=None):
        return cls._exp_of_none(name, key, value, exp_of_none=exp_of_none, callback=cls.conn.hincrby)

    @classmethod
    def hincrbyfloat(cls, name, key, value, exp_of_none=None):
        return cls._exp_of_none(name, key, value, exp_of_none=exp_of_none, callback=cls.conn.hincrbyfloat)

    @classmethod
    def hget(cls, name, key, default=0):
        """
        缓存清除，接收list or str
        :param name:
        :param default:
        :param key:
        :return:
        """
        v = cls.conn.hget(name, key)
        if v is None:
            return default
        return v.decode()


def join_params(params, key=None, filter_none=True, exclude_keys=None, sep='&', key_joint=True):
    """
    字典排序拼接参数
    :param key_joint: key是否加入排序
    :param sep:
    :param key: 签名key
    :param params:
    :param filter_none:
    :param exclude_keys: 排除参数
    :return:
    """
    tmp = []
    for p in sorted(params):
        value = params[p]
        if filter_none and value in [None, '']:
            continue
        if exclude_keys:
            if p in exclude_keys:
                continue
        tmp.append('{0}={1}'.format(p, value))
    if key_joint:
        if key:
            tmp.append('key={}'.format(key))
        ret = sep.join(tmp)
    else:
        ret = sep.join(tmp) + key
    return ret


def is_url(url):
    """
    校验是否合法的url
    :param url:
    :return:
    """
    return re.match(r'^https?:/{2}.+$', url)


def request_payment(url, payload, uaid, pay_key, method='POST'):
    """
    封装请求request_payment模块的方法
    :param uaid:
    :param pay_key:
    :param method:
    :param url:
    :param payload:
    :return:
    """
    payload['timestamp'] = int(time.time())
    payload['uaid'] = uaid
    payload['sign'] = md5_encode(join_params(payload, key=pay_key, sep=''))
    if method == 'POST':
        ret = requests.post(url, payload)
    elif method == 'GET':
        ret = requests.get(url, payload)
    else:
        raise NotImplementedError
    return ret.json()


def get_server_url(name, *args, **kwargs):
    """
    获取服务器链接
    :param name: 路由对应的name
    :return:
    """
    url = reverse(name, args=args, kwargs=kwargs)
    return settings.SERVER_URL + url


def datetime2timestamp(time_):
    """
    时间转时间戳
    :param time_:
    :return:
    """
    return int(time.mktime(time_.timetuple()))


def today_rest_seconds():
    """
    获取今天剩下的秒数
    :return:
    """
    return datetime2timestamp(datetime_now(d=-1).date()) - datetime2timestamp(datetime_now())
