import datetime
from django.db.models.aggregates import Sum
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import *
from Core.models import SystemInformation
from .forms import *
from django.contrib import messages
import weasyprint
from Engineering.models import *
from django.db.models import F


# Create your views here.

class CompanyList(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = Company
    paginate_by = 12

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=False).order_by('-id')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'list'
        context['title'] = 'قائمة '
        context['page'] = 'active'
        context['count'] = self.model.objects.filter(deleted=False).count()
        return context


class CompanyTrachList(LoginRequiredMixin, ListView):
    login_url = '/auth/login'
    model = Company
    paginate_by = 12

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=True).order_by('-id')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'trach'
        context['count'] = self.model.objects.filter(deleted=True).count()
        return context


class CompanyCreate(LoginRequiredMixin, CreateView):
    login_url = '/auth/login/'
    model = Company
    form_class = CompanyForm
    template_name = 'forms/form_template.html'
    success_url = reverse_lazy('Engineering:CompanyList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'اضافة شركة جديدة'
        context['message'] = 'add'
        context['action_url'] = reverse_lazy('Engineering:CompanyCreate')
        return context

    def get_success_url(self):
        messages.success(self.request, "تم اضافة شركة جديدة", extra_tags="success")

        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url


class CompanyUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = Company
    form_class = CompanyForm
    template_name = 'forms/form_template.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل شركة: ' + str(self.object)
        context['message'] = 'update'
        context['action_url'] = reverse_lazy('Engineering:CompanyUpdate', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self):
        messages.success(self.request, "تم تعديل شركة " + str(self.object) + " بنجاح ", extra_tags="success")
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url


class CompanyDelete(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = Company
    form_class = CompanyDeleteForm
    template_name = 'forms/form_template.html'

    def get_success_url(self):
        return reverse('Engineering:CompanyList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'نقل الشركة الي سلة المهملات: ' + str(self.object)
        context['message'] = 'delete'
        context['action_url'] = reverse_lazy('Engineering:CompanyDelete', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        messages.success(self.request, " تم نقل شركة " + str(self.object) + ' الي سلة المهملات بنجاح ', extra_tags="success")
        myform = Company.objects.get(id=self.kwargs['pk'])
        myform.deleted = 1
        myform.save()
        return redirect(self.get_success_url())


class CompanyRestore(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = Company
    form_class = CompanyDeleteForm
    template_name = 'forms/form_template.html'

    def get_success_url(self):
        return reverse('Engineering:CompanyTrachList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'استرجاع شركة: ' + str(self.object)
        context['message'] = 'restore'
        context['action_url'] = reverse_lazy('Engineering:CompanyRestore', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        messages.success(self.request, " تم استرجاع شركة " + str(self.object) + ' الي القائمة بنجاح ', extra_tags="success")
        myform = Company.objects.get(id=self.kwargs['pk'])
        myform.deleted = 0
        myform.save()
        return redirect(self.get_success_url())


class CompanySuperDelete(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = Company
    form_class = CompanyDeleteForm
    template_name = 'forms/form_template.html'

    def get_success_url(self):
        return reverse('Engineering:CompanyTrachList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'حذف شركة: ' + str(self.object)
        context['message'] = 'super_delete'
        context['action_url'] = reverse_lazy('Engineering:CompanySuperDelete', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        messages.success(self.request, " تم حذف شركة " + str(self.object) + " نهائيا بنجاح ", extra_tags="success")
        my_form = Company.objects.get(id=self.kwargs['pk'])
        my_form.delete()
        return redirect(self.get_success_url())


###############################################################

class GeoPlaceList(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = GeoPlace
    paginate_by = 12

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=False).order_by('-id')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'list'
        context['title'] = 'قائمة '
        context['page'] = 'active'
        context['count'] = self.model.objects.filter(deleted=False).count()
        return context


class GeoPlaceTrachList(LoginRequiredMixin, ListView):
    login_url = '/auth/login'
    model = GeoPlace
    paginate_by = 12

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=True).order_by('-id')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'trach'
        context['count'] = self.model.objects.filter(deleted=True).count()
        return context


class GeoPlaceCreate(LoginRequiredMixin, CreateView):
    login_url = '/auth/login/'
    model = GeoPlace
    form_class = GeoPlaceForm
    template_name = 'forms/form_template.html'
    success_url = reverse_lazy('Engineering:GeoPlaceList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'اضافة موقع جديد'
        context['message'] = 'add'
        context['action_url'] = reverse_lazy('Engineering:GeoPlaceCreate')
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class=self.form_class)
        form.fields['company'].queryset = Company.objects.filter(deleted=0, active=True)
        return form

    def form_valid(self, form):
        form.save()
        obj = form.save(commit=False)
        geo = GeoPlace.objects.get(id=obj.id)
        price_history = GeoPlacePriceHistory()
        price_history.geo = geo
        price_history.old_price = 0.0
        price_history.new_price = obj.price
        price_history.admin = self.request.user
        price_history.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        messages.success(self.request, "تم اضافة موقع جديد", extra_tags="success")

        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url


class GeoPlaceUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = GeoPlace
    form_class = GeoPlaceForm
    template_name = 'forms/form_template.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل موقع: ' + str(self.object)
        context['message'] = 'update'
        context['action_url'] = reverse_lazy('Engineering:GeoPlaceUpdate', kwargs={'pk': self.object.id})
        return context

    # def get_form(self, form_class=None):
    #     form = super().get_form(form_class=self.form_class)
    #     form.fields['company'].queryset = Company.objects.filter(deleted=0, active=True)
    #     return form

    def form_valid(self, form):
        geo = GeoPlace.objects.get(id=self.kwargs['pk'])
        form.save()
        obj = form.save(commit=False)
        price_history = GeoPlacePriceHistory()
        price_history.geo = geo
        price_history.old_price = geo.price
        price_history.new_price = obj.price
        price_history.admin = self.request.user
        price_history.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        messages.success(self.request, "تم تعديل موقع " + str(self.object) + " بنجاح ", extra_tags="success")
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url


class GeoPlaceDelete(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = GeoPlace
    form_class = GeoPlaceDeleteForm
    template_name = 'forms/form_template.html'

    def get_success_url(self):
        return reverse('Engineering:GeoPlaceList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'نقل الموقع الي سلة المهملات: ' + str(self.object)
        context['message'] = 'delete'
        context['action_url'] = reverse_lazy('Engineering:GeoPlaceDelete', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        messages.success(self.request, " تم نقل موقع " + str(self.object) + ' الي سلة المهملات بنجاح ', extra_tags="success")
        myform = GeoPlace.objects.get(id=self.kwargs['pk'])
        myform.deleted = 1
        myform.save()
        return redirect(self.get_success_url())


class GeoPlaceRestore(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = GeoPlace
    form_class = GeoPlaceDeleteForm
    template_name = 'forms/form_template.html'

    def get_success_url(self):
        return reverse('Engineering:GeoPlaceTrachList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'استرجاع موقع: ' + str(self.object)
        context['message'] = 'restore'
        context['action_url'] = reverse_lazy('Engineering:GeoPlaceRestore', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        messages.success(self.request, " تم استرجاع موقع " + str(self.object) + ' الي القائمة بنجاح ', extra_tags="success")
        myform = GeoPlace.objects.get(id=self.kwargs['pk'])
        myform.deleted = 0
        myform.save()
        return redirect(self.get_success_url())


class GeoPlaceSuperDelete(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = GeoPlace
    form_class = GeoPlaceDeleteForm
    template_name = 'forms/form_template.html'

    def get_success_url(self):
        return reverse('Engineering:GeoPlaceTrachList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'حذف موقع: ' + str(self.object)
        context['message'] = 'super_delete'
        context['action_url'] = reverse_lazy('Engineering:GeoPlaceSuperDelete', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        messages.success(self.request, " تم حذف موقع " + str(self.object) + " نهائيا بنجاح ", extra_tags="success")
        my_form = GeoPlace.objects.get(id=self.kwargs['pk'])
        my_form.delete()
        return redirect(self.get_success_url())


class GeoPlacePriceHistoryList(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = GeoPlacePriceHistory
    template_name = 'Engineering/geoplace_price_history.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        geo = GeoPlace.objects.get(id=self.kwargs['pk'])
        context['title'] = 'أسعار الموقع: ' + str(geo.name)
        context['type'] = 'list'
        context['prices'] = GeoPlacePriceHistory.objects.filter(geo=geo).order_by('-created', '-id')
        return context


####################################################################################

class SupplierList(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = Supplier
    paginate_by = 12

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=False).order_by('-id')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'list'
        context['title'] = 'قائمة '
        context['page'] = 'active'
        context['count'] = self.model.objects.filter(deleted=False).count()
        return context


class SupplierTrachList(LoginRequiredMixin, ListView):
    login_url = '/auth/login'
    model = Supplier
    paginate_by = 12

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=True).order_by('-id')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'trach'
        context['count'] = self.model.objects.filter(deleted=True).count()
        return context


class SupplierCreate(LoginRequiredMixin, CreateView):
    login_url = '/auth/login/'
    model = Supplier
    form_class = SupplierForm
    template_name = 'forms/form_template.html'
    success_url = reverse_lazy('Engineering:SupplierList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'اضافة مورد جديدة'
        context['message'] = 'add'
        context['action_url'] = reverse_lazy('Engineering:SupplierCreate')
        return context

    def get_success_url(self):
        messages.success(self.request, "تم اضافة مورد جديد", extra_tags="success")

        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url


class SupplierUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = Supplier
    form_class = SupplierForm
    template_name = 'forms/form_template.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل مورد: ' + str(self.object)
        context['message'] = 'update'
        context['action_url'] = reverse_lazy('Engineering:SupplierUpdate', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self):
        messages.success(self.request, "تم تعديل المورد " + str(self.object) + " بنجاح ", extra_tags="success")
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url


class SupplierDelete(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = Supplier
    form_class = SupplierFormDelete
    template_name = 'forms/form_template.html'

    def get_success_url(self):
        return reverse('Engineering:SupplierList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'نقل المورد الي سلة المهملات: ' + str(self.object)
        context['message'] = 'delete'
        context['action_url'] = reverse_lazy('Engineering:SupplierDelete', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        messages.success(self.request, " تم نقل المورد " + str(self.object) + ' الي سلة المهملات بنجاح ', extra_tags="success")
        myform = Supplier.objects.get(id=self.kwargs['pk'])
        myform.deleted = 1
        myform.save()
        return redirect(self.get_success_url())


class SupplierRestore(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = Supplier
    form_class = SupplierFormDelete
    template_name = 'forms/form_template.html'

    def get_success_url(self):
        return reverse('Engineering:SupplierTrachList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'استرجاع مورد: ' + str(self.object)
        context['message'] = 'restore'
        context['action_url'] = reverse_lazy('Engineering:SupplierRestore', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        messages.success(self.request, " تم استرجاع المورد " + str(self.object) + ' الي القائمة بنجاح ', extra_tags="success")
        myform = Supplier.objects.get(id=self.kwargs['pk'])
        myform.deleted = 0
        myform.save()
        return redirect(self.get_success_url())


class SupplierSuperDelete(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = Supplier
    form_class = SupplierFormDelete
    template_name = 'forms/form_template.html'

    def get_success_url(self):
        return reverse('Engineering:SupplierTrachList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'حذف مورد: ' + str(self.object)
        context['message'] = 'super_delete'
        context['action_url'] = reverse_lazy('Engineering:SupplierSuperDelete', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        messages.success(self.request, " تم حذف المورد " + str(self.object) + " نهائيا بنجاح ", extra_tags="success")
        my_form = Supplier.objects.get(id=self.kwargs['pk'])
        my_form.delete()
        return redirect(self.get_success_url())