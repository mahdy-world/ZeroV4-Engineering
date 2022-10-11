from Core.models import SystemInformation
from Engineering.models import *
from Factories.models import Factory
from Invoices.models import *
from django.db.models import F
from Workers.models import Worker
from Core.models import *


def allcontext(request):
    info = SystemInformation.objects.filter(id=1)
    factorys = Factory.objects.filter(deleted=False)
    products = Product.objects.filter(deleted=False)
    sellers = ProductSellers.objects.filter(deleted=False)
    allsellers = ProductSellers.objects.all()
    workers = Worker.objects.filter(deleted=False)
    suppliers = Supplier.objects.filter(deleted=False)

    invoices_notify = Invoice.objects.filter(saved=False)
    products_notify = Product.objects.filter(price__lt=F('cost'))

    notification_count = invoices_notify.count() + products_notify.count()

    modules = Modules.objects.all().last()

    companies = Company.objects.filter(deleted=False)
    geoplaces = GeoPlace.objects.filter(deleted=False)
    context = {
        'info':info,
        'factorys' : factorys,
        'suppliers' : suppliers,
        'products':products,
        'sellers':sellers,
        'allsellers':allsellers,
        'workers':workers,
        'invoices_notify':invoices_notify,
        'products_notify':products_notify,
        'notification_count':notification_count,
        'modules':modules,
        'companies': companies,
        'geoplaces': geoplaces,
    }
    return context