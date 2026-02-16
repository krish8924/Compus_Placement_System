from django import template

register = template.Library()

@register.filter
def split(value, arg):
    """
    Split a string by the specified delimiter
    Usage: {{ value|split:',' }}
    """
    return value.split(arg)

@register.filter
def strip(value):
    """
    Strip whitespace from a string
    Usage: {{ value|strip }}
    """
    return value.strip()