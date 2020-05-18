from urllib.parse import parse_qs, quote

from poverty.common import join_params, md5_encode


def verify_sign(params, private_key):
    """
    校验sign
    :param params:
    :param private_key:
    :return:
    """
    sign = params.get('sign')
    sign_str = join_params(params, key=private_key, sep='', exclude_keys=['sign'])
    sign_tmp = md5_encode(sign_str)
    return sign == sign_tmp


def get_ip(request):
    """
    获取客户端真实ip
    :param request:
    :return:
    """
    if request.META.get('HTTP_X_FORWARDED_FOR'):
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    return ip.split(',')[0]


def overwrite_request(request):
    """
    覆盖request方法，重写sign和timestamp参数以支持缓存
    :param request:
    :return:
    """
    if request.method == 'GET':
        query_string = request.META['QUERY_STRING']
        qs = parse_qs(query_string)
        qs.pop('sign', '')
        qs.pop('timestamp', '')
        qs_list = []
        for k in qs:
            qs_list.append(f'{k}={quote(qs.get(k)[0])}')
        token = request.headers.get('Authorization')
        if token:
            qs_list.append(f'token={token}')
        request.META['QUERY_STRING'] = '&'.join(qs_list)
    return request
