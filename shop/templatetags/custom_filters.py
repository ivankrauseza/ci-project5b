from django import template
from django.utils.text import slugify

register = template.Library()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def custom_slugify(value):
    return slugify(value)


@register.filter
def floatmultiply(value, arg):
    try:
        return float(value) * float(arg)
    except (TypeError, ValueError):
        return 0.0
