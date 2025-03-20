from django import template
register = template.Library()
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

# templatetags/custom_filters.py
@register.filter
def ratio(value, total):
    """计算百分比"""
    try:
        return (value / total) * 100
    except ZeroDivisionError:
        return 0