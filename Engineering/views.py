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

    def get_success_url(self):
        messages.success(self.request, "تم اضافة شركة جديدة", extra_tags="success")

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