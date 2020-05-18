from tortoise import fields

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
    name = fields.CharField(max_length=50, description="姓名")
    phone = fields.CharField(max_length=20, description="电话号码")
    email = fields.CharField(max_length=50, description="邮箱地址")
    balance = fields.DecimalField(max_digits=10, decimal_places=4, default=0, description="账户余额")
