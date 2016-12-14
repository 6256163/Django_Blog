from django.template.defaultfilters import stringfilter

__author__ = 'TT'
from django import template

register = template.Library()

@register.filter('list')
def do_list(value):
    """
    translate an int/float value to list
    eg:
    int value - 10
    list - [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    float value 10.5
    list - [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    """
    return range(1, int(value)+1 if int(value)==value else int(value)+2)

@register.filter('divide')
def divided_by(dividend, divisor):
    return dividend/float(divisor)
