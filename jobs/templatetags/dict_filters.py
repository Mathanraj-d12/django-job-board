from django import template

register = template.Library()

@register.filter
def dict_get(d, key):
    """Returns the value of key in a dictionary or None."""
    return d.get(key)
