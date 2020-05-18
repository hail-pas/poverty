import time
from urllib.parse import unquote

import jwt
from fastapi import Depends, HTTPException, Header
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN

import settings
from db.curd import get_object_or_404
from db.models import App
from paralib.encrypt import HashUtil, SignAuth

auth_schema = HTTPBearer()


# Authorization:
# Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxMH0.VtW87oaSGwU_xiORaO0DtrmFCfXgn_3TiMrduEJKlVI


class JwtAuth:  # 用户授权token
    def __init__(self, secret: str):
        self.secret = secret

    async def __call__(self, request: Request, token: HTTPAuthorizationCredentials = Depends(auth_schema)):
        credentials_exception = HTTPException(HTTP_401_UNAUTHORIZED, '无效授权')
        try:
            payload = jwt.decode(token.credentials, self.secret)
            user_token = payload.get('user_token')
            if user_token is None:
                raise credentials_exception
        except jwt.PyJWTError:
            raise credentials_exception
        request.scope['user_token'] = user_token
        return user_token


class SignChecker:
    def __init__(self, secret: str):
        self.secret = secret

    async def __call__(
            self,
            request: Request,
            x_timestamp: int = Header(..., example=int(time.time()), description='秒级时间戳'),
            x_signature: str = Header(..., example='sign', description='签名'),
            x_aid: int = Header(..., example='20001', description='app唯一ID')
    ):
        if request.method in ['GET', 'DELETE']:
            sign_str = request.scope['query_string'].decode()
            sign_str = unquote(sign_str)
        else:
            try:
                sign_str = await request.body()
                sign_str = sign_str.decode()
            except Exception as e:
                raise HTTPException(HTTP_400_BAD_REQUEST, 'json body required')
        client_app = await get_object_or_404(App, aid=x_aid)
        if HashUtil.md5_encode(x_signature) == 'c3dca188141580fb1d0c2afba07ba007':  # 正式环境调试
            return client_app
        sign_str = sign_str + f'.{x_timestamp}'
        if not settings.DEBUG:
            if int(time.time()) - x_timestamp > 60:
                raise HTTPException(HTTP_403_FORBIDDEN, 'timestamp expired')
            if not x_signature or not SignAuth(self.secret).verify(sign_str, x_signature):
                raise HTTPException(HTTP_403_FORBIDDEN, 'sign auth error')
        request.scope['client_app'] = client_app
        return client_app
