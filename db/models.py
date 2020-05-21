from tortoise import fields

from db import enums
from db.base import BaseModel


class App(BaseModel):
    aid = fields.IntField(unique=True)
    label = fields.CharField(max_length=20)
    pay_key = fields.CharField(max_length=50, description="pay key")
    announcement = fields.TextField(verbose_name='公告')
    service = fields.TextField(verbose_name='服务条款')


class User(BaseModel):
    app = fields.ManyToManyField("models.App", related_name="users")
    token = fields.CharField(max_length=20, unique=True, description="认证token")
    password = fields.CharField(max_length=200)
    name = fields.CharField(max_length=50, description="姓名")
    phone = fields.CharField(max_length=20, description="电话号码")
    email = fields.CharField(max_length=50, description="邮箱地址")
    balance = fields.DecimalField(max_digits=10, decimal_places=4, default=0, description="账户余额")


class Config(BaseModel):
    label = fields.CharField(max_length=200, description="标签")
    key = fields.CharField(max_length=20, description="key")
    value = fields.JSONField(description="value")
    status: enums.GeneralStatus = fields.IntEnumField(enums.GeneralStatus, default=enums.GeneralStatus.on)


class Admin(BaseModel):
    username = fields.CharField(max_length=20, unique=True)
    password = fields.CharField(max_length=200)
    mobile = fields.CharField(max_length=200, default="")
    avatar = fields.CharField(max_length=200, default="")
    last_login = fields.DatetimeField(description='上次登录')
    is_active = fields.BooleanField(default=True, description='是否激活')
    is_superuser = fields.BooleanField(default=False, description='超级管理员')


class Role(BaseModel):
    label = fields.CharField(max_length=50)
    admin = fields.ManyToManyField('models.Admin')
