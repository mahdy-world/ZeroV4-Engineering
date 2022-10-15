from Core.models import SystemInformation
from Engineering.models import *
from django.db.models import F
from Core.models import *


def allcontext(request):
    info = SystemInformation.objects.filter(id=1)
    modules = Modules.objects.all().last()
    companies = Company.objects.filter(deleted=False)
    geoplaces = GeoPlace.objects.filter(deleted=False)
    suppliers = Supplier.objects.filter(deleted=False)
    sheets = Sheet.objects.filter(deleted=False)
    context = {
        'info':info,
        'modules':modules,
        'companies': companies,
        'geoplaces': geoplaces,
        'suppliers': suppliers,
        'sheets': sheets,
    }
    return context