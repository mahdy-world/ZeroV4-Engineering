from Engineering.models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import *
from django.contrib import messages
from Core.forms import SystemInfoForm
from Core.models import SystemInformation
from Products.models import *
from Factories.models import Factory, Supplier
from Workers.models import Worker
from Invoices.models import Invoice
from Core.models import *
# Create your views here.


@login_required(login_url='Auth:login')
def Index(request):
    modules = Modules.objects.all().last()
    return render(request, 'core/index.html', {'modules':modules})


class SystemInfoCreate(LoginRequiredMixin, CreateView):
    login_url = '/auth/login/'
    model = SystemInformation
    template_name = 'forms/form_template.html'
    form_class = SystemInfoForm
    success_url = reverse_lazy('Core:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'بيانات النظام'
        context['message'] = 'info'
        context['action_url'] = reverse_lazy('Core:SystemInfoCreate')
        return context
    
    def get_success_url(self):
        messages.success(self.request, "  تم إضافة بيانات للنظام بنجاح", extra_tags="success")

        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url
        # return reverse('Core:index')
    
    
class SystemInfoUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = SystemInformation
    template_name = 'forms/form_template.html'
    form_class = SystemInfoForm
    success_url = reverse_lazy('Core:index')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل بيانات النظام'
        context['message'] = 'info'
        context['info_obj'] = self.object
        context['action_url'] = reverse_lazy('Core:SystemInfoUpdate',kwargs={'pk': self.object.id})
        return context
    
    def get_success_url(self):
        messages.success(self.request, " تم تعديل بيانات النظام بنجاح", extra_tags="success")

        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url
        # return reverse('Core:index')


class FactorySearch(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = Factory
    template_name = 'Factory/factory_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'active'
        context['page'] = 'active'
        context['search'] = self.request.GET.get("factory")
        context['type'] = 'list'
        context['count'] = self.model.objects.filter(deleted=False).count()
        return context
    
    def get_queryset(self):
        search = self.request.GET.get("factory")  
        queryset = self.model.objects.filter(name__icontains=search, deleted=False)
        return queryset
    
    
class ProductSearch(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = Product
    template_name = 'Products/product_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'active'
        context['page'] = 'active'
        context['product_serach'] = self.request.GET.get("product")
        context['type'] = 'list'
        context['count'] = self.model.objects.filter(deleted=False).count()
        return context
    
    def get_queryset(self):
        product_serach = self.request.GET.get("product")  
        queryset = self.model.objects.filter(name__icontains=product_serach, deleted=False)
        return queryset


class InvoiceSearch(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = Invoice
    template_name = 'Invoices/invoice_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'active'
        if self.model.objects.filter(id=int(self.request.GET.get("invoice")), deleted=False):
            inv_type = self.model.objects.get(id=int(self.request.GET.get("invoice")), deleted=False).invoice_type
            context['type'] = inv_type
            context['count'] = self.model.objects.filter(deleted=False, invoice_type=inv_type).count()
        else:
            context['type'] = 1
            context['count'] = self.model.objects.filter(deleted=False, invoice_type=1).count()
        context['invoice_serach'] = self.request.GET.get("invoice")
        return context

    def get_queryset(self):
        invoice_serach = self.request.GET.get("invoice")
        queryset = self.model.objects.filter(id=int(invoice_serach), deleted=False)
        if queryset:
            inv_type = self.model.objects.get(id=int(invoice_serach), deleted=False).invoice_type
            queryset = queryset.filter(invoice_type=inv_type)
        else:
            queryset = self.model.objects.filter(deleted=False, invoice_type=1)
        return queryset


class SpInvoiceSearch(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = Invoice
    template_name = 'Invoices/invoice_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'active'
        context['type'] = self.kwargs['type']
        context['invoice_serach'] = self.request.GET.get("invoice")
        context['count'] = self.model.objects.filter(deleted=False, invoice_type=int(self.kwargs['type'])).count()
        return context

    def get_queryset(self):
        invoice_serach = self.request.GET.get("invoice")
        queryset = self.model.objects.filter(id=int(invoice_serach), deleted=False, invoice_type=int(self.kwargs['type']))
        if queryset:
            queryset = queryset
        else:
            queryset = self.model.objects.filter(deleted=False, invoice_type=int(self.kwargs['type']))
        return queryset


class WorkerSearch(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = Worker
    template_name = 'Worker/worker_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'active'
        context['page'] = 'active'
        context['worker_serach'] = self.request.GET.get("worker")
        context['type'] = 'list'
        context['count'] = self.model.objects.filter(deleted=False).count()
        return context
    
    def get_queryset(self):
        worker_serach = self.request.GET.get("worker")  
        queryset = self.model.objects.filter(name__icontains=worker_serach, deleted=False)
        return queryset


class SellerSearch(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = ProductSellers
    paginate_by = 6

    def get_queryset(self):
        seller = self.request.GET.get('seller')
        queryset = self.model.objects.filter(deleted=False, name__icontains=str(seller)).order_by('-id')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'list'
        context['title'] = 'قائمة التجار'
        context['seller_serach'] = self.request.GET.get('seller')
        context['page'] = 'active'
        context['seller_search'] = self.request.GET.get('seller')
        context['count'] = self.model.objects.filter(deleted=False).count()
        return context


class SpSupplierSearch(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = Supplier
    template_name = 'Supplier/supplier_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'active'
        context['type'] = self.kwargs['type']
        context['search'] = self.request.GET.get("supplier")
        context['count'] = self.model.objects.filter(deleted=False, type=int(self.kwargs['type'])).count()
        return context

    def get_queryset(self):
        search = self.request.GET.get("supplier")
        queryset = self.model.objects.filter(name=search, deleted=False, type=int(self.kwargs['type']))
        if queryset:
            queryset = queryset
        else:
            queryset = self.model.objects.filter(deleted=False, type=int(self.kwargs['type']))
        return queryset


class SellerInvoiceSearch(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = Invoice
    template_name = 'Invoices/invoice_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'active'
        context['type'] = self.kwargs['type']
        context['seller_invoice_search'] = self.request.GET.get("seller_invoice")
        context['count'] = self.model.objects.filter(deleted=False, invoice_type=int(self.kwargs['type'])).count()
        return context

    def get_queryset(self):
        seller_invoice_search = self.request.GET.get("seller_invoice")
        queryset = self.model.objects.filter(seller__name__icontains=seller_invoice_search, deleted=False, invoice_type=int(self.kwargs['type']))
        if queryset:
            queryset = queryset
        else:
            messages.error(self.request, "خطأ! لايوجد فواتير لهذا التاجر ", extra_tags="danger")
            queryset = self.model.objects.filter(deleted=False, invoice_type=int(self.kwargs['type']))
        return queryset


class ClientInvoiceSearch(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = Invoice
    template_name = 'Invoices/invoice_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'active'
        context['type'] = self.kwargs['type']
        context['client_invoice_search'] = self.request.GET.get("client_invoice")
        context['count'] = self.model.objects.filter(deleted=False, invoice_type=int(self.kwargs['type'])).count()
        return context

    def get_queryset(self):
        client_invoice_search = self.request.GET.get("client_invoice")
        queryset = self.model.objects.filter(customer__icontains=client_invoice_search, deleted=False, invoice_type=int(self.kwargs['type']))
        if queryset:
            queryset = queryset
        else:
            messages.error(self.request, "خطأ! لايوجد فواتير لهذا العميل ", extra_tags="danger")
            queryset = self.model.objects.filter(deleted=False, invoice_type=int(self.kwargs['type']))
        return queryset


class CompanySearch(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = Company
    template_name = 'Engineering/company_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'active'
        context['page'] = 'active'
        context['company_search'] = self.request.GET.get("company")
        context['type'] = 'list'
        context['count'] = self.model.objects.filter(deleted=False).count()
        return context

    def get_queryset(self):
        company_search = self.request.GET.get("company")
        queryset = self.model.objects.filter(name__icontains=company_search, deleted=False)
        if queryset:
            return queryset
        else:
            messages.error(self.request, "لاتوجد شركة بهذا الإسم .. ابحث في سلة المهملات", extra_tags="danger")
            return self.model.objects.filter(deleted=False)


class SupplierSearch(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = Supplier
    template_name = 'Engineering/supplier_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'active'
        context['page'] = 'active'
        context['supplier_search'] = self.request.GET.get("supplier")
        context['type'] = 'list'
        context['count'] = self.model.objects.filter(deleted=False).count()
        return context

    def get_queryset(self):
        supplier_search = self.request.GET.get("supplier")
        queryset = self.model.objects.filter(name__icontains=supplier_search, deleted=False)
        if queryset:
            return queryset
        else:
            messages.error(self.request, "لا يوجد مورد بهذا الإسم .. ابحث في سلة المهملات", extra_tags="danger")
            return self.model.objects.filter(deleted=False)


class GeoPlaceSearch(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = GeoPlace
    template_name = 'Engineering/geoplace_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'active'
        context['page'] = 'active'
        context['geoplace_search'] = self.request.GET.get("geoplace")
        context['type'] = 'list'
        context['count'] = self.model.objects.filter(deleted=False).count()
        return context

    def get_queryset(self):
        geoplace_search = self.request.GET.get("geoplace")
        queryset = self.model.objects.filter(name__icontains=geoplace_search, deleted=False)
        if queryset:
            return queryset
        else:
            messages.error(self.request, "لايوجد موقع بهذا الإسم .. ابحث في سلة المهملات", extra_tags="danger")
            return self.model.objects.filter(deleted=False)


class CompanyGeosSearch(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = GeoPlace
    template_name = 'Engineering/geoplace_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'active'
        context['page'] = 'active'
        context['company_geo_search'] = self.request.GET.get("company_geo")
        context['type'] = 'list'
        context['count'] = self.model.objects.filter(deleted=False).count()
        return context

    def get_queryset(self):
        company_geo_search = self.request.GET.get("company_geo")
        queryset = self.model.objects.filter(company__name__icontains=company_geo_search, deleted=False)
        if queryset:
            return queryset
        else:
            messages.error(self.request, "لاتوجد مواقع لهذه الشركة .. ابحث في سلة المهملات", extra_tags="danger")
            return self.model.objects.filter(deleted=False)