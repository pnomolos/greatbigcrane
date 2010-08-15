
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def configvalue(item):
    '''If a config value is a string, return it, if list, newline it, if
    tuples, let jason figure it out.'''
    if isinstance(item, list):
        return mark_safe('<br />&nbsp;&nbsp;&nbsp;'.join(item))
    return item
