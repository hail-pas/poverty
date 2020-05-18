from typing import TypeVar
from tortoise import Model, fields

MODEL = TypeVar("MODEL", bound="Model")


class BaseModel(Model):
    created_at = fields.DatetimeField(auto_now_add=True, description='创建时间')
    updated_at = fields.DatetimeField(auto_now=True, description='更新时间')

    class Meta:
        abstract = True
