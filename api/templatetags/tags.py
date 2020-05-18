from django import template

register = template.Library()


@register.filter
def pre_item(lists, index):
    return lists[index - 1]


@register.simple_tag
def update_value(value):
    return value
