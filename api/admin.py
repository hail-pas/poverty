from html import escape
from django.contrib import admin
from django.contrib.admin.models import DELETION, LogEntry
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User as AuthUser
from django.urls import reverse
from django.utils import safestring
from rangefilter.filter import DateTimeRangeFilter

from api import models
from poverty.admin import SearchPlaceholderAdmin


@admin.register(LogEntry)
class LogEntryAdmin(SearchPlaceholderAdmin):
    list_filter = [
        'user',
        'content_type',
        'action_flag',
        ('action_time', DateTimeRangeFilter)
    ]
    readonly_fields = [
        'user',
        'action_time',
        'content_type',
        'object_link',
        'action_flag_',
        'change_message',
    ]
    suit_list_filter_horizontal = list_filter

    search_fields = [
        'object_repr',
        'change_message'
    ]

    list_display = [
        'id',
        'user',
        'action_time',
        'content_type',
        'object_link',
        'action_flag_',
        'change_message',
    ]

    def action_flag_(self, obj):
        flags = {
            1: '新增',
            2: '修改',
            3: '删除',
        }
        return flags[obj.action_flag]

    action_flag_.short_description = '动作'

    def object_link(self, obj):
        if obj.action_flag == DELETION:
            return escape(obj.object_repr)
        else:
            ct = obj.content_type
            return safestring.mark_safe('<a href="%s">%s</a>' % (
                reverse('admin:%s_%s_change' % (ct.app_label, ct.model), args=[obj.object_id]),
                escape(obj.object_repr),
            ))

    object_link.allow_tags = True
    object_link.admin_order_field = 'object_repr'
    object_link.short_description = '修改对象'


# class ReturnVisitInline(admin.TabularInline):
#     model = models.ReturnVisit
#     extra = 3
#
#
# @admin.register(models.User)
# class UserAdmin(SearchPlaceholderAdmin):
#     list_display = []
#     search_fields = []
#     list_editable = []
#     inlines = [ReturnVisitInline]
#     list_filter = ['app', ('create', DateTimeRangeFilter)]
#     raw_id_fields = ['parent']
#     suit_list_filter_horizontal = list_filter
#
#     def save_model(self, request, obj: models.User, form, change):
#         if not change:
#             obj.password = make_password(obj.password)
#         else:
#             changed_data = form.changed_data or []
#             if 'password' in changed_data:
#                 obj.password = make_password(obj.password)
#             user = models.User.objects.get(pk=obj.pk)
#             change_score = obj.balance - user.balance
#         super(UserAdmin, self).save_model(request, obj, form, change)
#
#     def suit_row_attributes(self, obj, request):
#         css = {
#             2: 'table-info',
#             3: 'table-warning'
#         }.get(obj.status)
#         if css:
#             return {'class': css}
#
#     def order_create(self, obj):
#         order = models.Order.objects.filter(user=obj, status=2).last()
#         if order:
#             return order.create
#         return ''
#
#     order_create.short_description = 'name'
#     order_create.allow_tags = True
