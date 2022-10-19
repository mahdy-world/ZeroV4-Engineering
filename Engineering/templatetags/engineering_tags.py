from django import template
from django.db.models import Sum
from Engineering.models import Bon

register = template.Library()
from django.db.models import F

@register.simple_tag(name='company_has_bons')
def company_has_bons(id):
    bons = Bon.objects.filter(sheet__company__id=id)
    return bons


@register.simple_tag(name='geo_has_bons')
def geo_has_bons(id):
    bons = Bon.objects.filter(geo_place__id=id)
    return bons


@register.simple_tag(name='supplier_has_bons')
def supplier_has_bons(id):
    bons = Bon.objects.filter(sheet__supplier__id=id)
    return bons