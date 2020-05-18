import json

from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse, HttpResponse
from rest_framework.pagination import PageNumberPagination

from poverty.common import AESUtil

ERR_MSG_DICT = {
    401: 'token校验失败',
    403: '未授权',
    405: '请求方法不被允许',
    412: 'sign校验失败',
    415: '参数校验失败',
    420: '缺少必填参数',
    428: '无法删除',
    429: '已存在',
    430: '验证码错误',
    431: '价格错误',
    432: '余额不足',
    433: '创建失败',
    434: '无法更新',
    435: '查询失败'
}


class JSONResponse(JsonResponse):
    def __init__(self, data=None, msg=None, encoder=DjangoJSONEncoder, safe=False,
                 json_dumps_params=None, **kwargs):
        status = kwargs.get('status') or 200
        ret = {
            'code': status,
        }
        if status == 200:
            if data is not None:
                ret['data'] = data
        else:
            err = ERR_MSG_DICT.get(int(status))
            if msg:
                msg = '{}'.format(msg)
            else:
                msg = err
            ret['msg'] = msg
        super(JSONResponse, self).__init__(ret, encoder=encoder, safe=safe,
                                           json_dumps_params=json_dumps_params, **kwargs)


class AESJsonResponse(HttpResponse):
    def __init__(self, data=None, msg=None, *args, **kwargs):
        status = kwargs.get('status') or 200
        ret = {
            'code': status,
        }
        if status != 200:
            err = ERR_MSG_DICT.get(int(status))
            if msg:
                msg = '{}'.format(msg)
            else:
                msg = err
            ret['msg'] = msg
        if data is not None:
            ret['data'] = data
        content = json.dumps(ret, cls=DjangoJSONEncoder, ensure_ascii=False, )
        if not settings.DEBUG:
            content = AESUtil().encrypt_data(content)
            super(AESJsonResponse, self).__init__(content=content, *args,
                                                  **kwargs)
        else:
            super(AESJsonResponse, self).__init__(content=content, content_type='application/json', *args,
                                                  **kwargs)


class PageNumberSizePagination(PageNumberPagination):
    page_size_query_param = 'num'
