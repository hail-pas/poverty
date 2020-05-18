from django.contrib import admin
from django.core.exceptions import FieldDoesNotExist


class SearchPlaceholderAdmin(admin.ModelAdmin):
    def get_changelist_instance(self, request):
        instance = super().get_changelist_instance(request)
        search_str_list = []
        for x in instance.search_fields:
            try:
                str_item = self.model._meta.get_field(x).verbose_name.title()
            except FieldDoesNotExist:
                model_str, field_str = x.split('__')
                str_item = self.model._meta.get_field(model_str).related_model._meta.get_field(
                    field_str).verbose_name.title()
            search_str_list.append(str_item)
        search_str = '、'.join(search_str_list)
        instance.placeholder = f'按照 {search_str} 搜索'
        return instance
