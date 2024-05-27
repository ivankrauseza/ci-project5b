from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def floatmultiply(value, arg):
    try:
        return float(value) * float(arg)
    except (TypeError, ValueError):
        return 0.0
