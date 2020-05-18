from typing import Generic

from fastapi import HTTPException
from starlette.status import HTTP_404_NOT_FOUND
from tortoise.exceptions import DoesNotExist
from tortoise.models import MODEL


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
