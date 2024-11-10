"""Custom_filters.py"""

from decimal import Decimal
from django import template

register = template.Library()

@register.filter(name='abs_value')
def abs_value(value):
    """returns the abs value of the given value"""
    return abs(Decimal(value))
