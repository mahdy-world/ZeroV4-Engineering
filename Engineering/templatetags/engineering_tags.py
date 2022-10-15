from django import template
from django.db.models import Sum

register = template.Library()
from django.db.models import F

@register.simple_tag(name='func')
def func(id):
    return 'none'