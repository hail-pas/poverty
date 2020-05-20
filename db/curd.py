from typing import Generic

from fastapi import HTTPException
from starlette.status import HTTP_404_NOT_FOUND
from tortoise.exceptions import DoesNotExist
from tortoise.models import MODEL

from db.models import Config


async def get_object_or_404(model: Generic[MODEL], **kwargs):
    """
    快捷get方法
    :param model:
    :param kwargs:
    :return:
    """
    try:
        obj = await model.get(**kwargs)  # type:model
        return obj
    except DoesNotExist as e:
        raise HTTPException(HTTP_404_NOT_FOUND, 'Not Found')


async def get_config_by_key(key, default=None):
    """
    获取在线参数
    :param key:
    :param default:
    :return:
    """
    config = await Config.get_or_none(key=key)
    if not config:
        return default
    return config.value
