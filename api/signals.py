from django.db.models import F
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.shortcuts import get_object_or_404

from api import models, cache

# @receiver(post_save, sender=models.model)
# def model_save(sender, **kwargs):
#     """
#     model保存信号
#     :param sender:
#     :param kwargs:
#     :return:
#     """
#     config = kwargs.get('instance')  # type:models.model
#     update_fields = kwargs.get('update_fields') or []
#     created = kwargs.get('created')
