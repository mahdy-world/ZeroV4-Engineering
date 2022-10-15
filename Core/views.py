from Engineering.models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import *
from django.contrib import messages
from Core.forms import SystemInfoForm
from Core.models import SystemInformation
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