from tortoise.signals import post_save

from db import models


# @post_save(models.App)
# async def invoice_save(sender, instance: models.App, created: bool, using_db, update_fields):
#     """
#     保存信号
#     """
