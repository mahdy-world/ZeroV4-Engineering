from django import template
from Engineering.models import Bon

register = template.Library()

@register.simple_tag(name='company_has_bons')
def company_has_bons(id):
    bons = Bon.objects.filter(company__id=id, sheet__deleted=0)
    return bons


@register.simple_tag(name='geo_has_bons')
def geo_has_bons(id):
    bons = Bon.objects.filter(geo_place__id=id, sheet__deleted=0)
    return bons


@register.simple_tag(name='supplier_has_bons')
def supplier_has_bons(id):
    bons = Bon.objects.filter(sheet__supplier__id=id, sheet__deleted=0)
    return bons