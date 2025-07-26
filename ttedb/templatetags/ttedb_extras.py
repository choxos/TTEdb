from django import template

register = template.Library()

@register.filter
def split(value, delimiter):
    """Split a string by delimiter"""
    if value:
        return value.split(delimiter)
    return []

@register.filter 
def trim(value):
    """Remove leading and trailing whitespace"""
    if value:
        return value.strip()
    return value

@register.filter
def truncatechars(value, length):
    """Truncate string to specified length"""
    if value and len(value) > length:
        return value[:length] + '...'
    return value

@register.filter
def widthratio(value, max_value, max_width):
    """Calculate width ratio for progress bars"""
    try:
        return int((value / max_value) * max_width)
    except (ValueError, ZeroDivisionError):
        return 0 