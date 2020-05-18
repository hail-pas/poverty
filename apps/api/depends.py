from arq import ArqRedis
from fastapi import Depends, Query, HTTPException
from fastapi.security import HTTPBearer
from pydantic import PositiveInt
from starlette.requests import Request
from starlette.status import HTTP_404_NOT_FOUND

import settings
from apps.depends import JwtAuth, SignChecker
from apps.types import Pager
from db.models import User

auth_schema = HTTPBearer()

jwt_required = JwtAuth(settings.API_SECRET)
sign_required = SignChecker(settings.API_SECRET)


async def get_client_app(app=Depends(sign_required)):
    return app


def get_pager(page: PositiveInt = Query(..., example=1, description='第几页'),
              size: PositiveInt = Query(..., example=10, description='每页数量')):
    return Pager(limit=size, offset=(page - 1) * size)


async def get_current_user(user_token=Depends(jwt_required)):
    user = await User.get_or_none(user_token=user_token)
    if not user:
        raise HTTPException(HTTP_404_NOT_FOUND)
    return user


async def get_arq(request: Request) -> ArqRedis:
    return request.app.arq
