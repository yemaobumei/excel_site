from django import template
register = template.Library()
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def ratio(value, max_value):
    """计算百分比"""
    try:
        return (value / max_value) * 100
    except ZeroDivisionError:
        return 0