__author__ = 'TT'
from django import template

register = template.Library()

@register.filter('list')
def do_list(value):
    return range(1, int(value)+1 if int(value)==value else int(value)+2)

@register.filter('divide')
def divided_by(dividend, divisor):
    return dividend/float(divisor)