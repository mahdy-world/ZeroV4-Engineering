import datetime
from django.db.models.aggregates import Sum, Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
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

        material_price_history = GeoPlaceMaterialPriceHistory()
        material_price_history.geo = geo
        material_price_history.old_price = 0.0
        material_price_history.new_price = obj.material_price
        material_price_history.admin = self.request.user
        material_price_history.save()
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
        if geo.price != obj.price:
            price_history = GeoPlacePriceHistory()
            price_history.geo = geo
            price_history.old_price = geo.price
            price_history.new_price = obj.price
            price_history.admin = self.request.user
            price_history.save()

        if geo.material_price != obj.material_price:
            material_price_history = GeoPlaceMaterialPriceHistory()
            material_price_history.geo = geo
            material_price_history.old_price = geo.material_price
            material_price_history.new_price = obj.material_price
            material_price_history.admin = self.request.user
            material_price_history.save()
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


def GeoPlacePriceHistoryList(request, pk):
    geo = GeoPlace.objects.get(id=pk)
    title = 'أسعار الموقع / أسعار الخامة: ' + str(geo.name)
    type = 'list'
    prices = GeoPlacePriceHistory.objects.filter(geo=geo).order_by('-created', '-id')
    material_prices = GeoPlaceMaterialPriceHistory.objects.filter(geo=geo).order_by('-created', '-id')
    return render(request, 'Engineering/More/geoplace_price_history.html', {
        'title': title,
        'type': type,
        'prices': prices,
        'material_prices': material_prices,
    })

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
        context['title'] = 'اضافة مورد جديد'
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


###################################################################

class SheetList(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = Sheet
    paginate_by = 12

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=False).order_by('-id')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'list'
        context['title'] = 'قائمة'
        context['page'] = 'active'
        context['count'] = self.model.objects.filter(deleted=False).count()
        return context


class SheetTrashList(LoginRequiredMixin, ListView):
    login_url = '/auth/login'
    model = Sheet
    paginate_by = 12

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=True).order_by('-id')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'trach'
        context['count'] = self.model.objects.filter(deleted=True).count()
        return context


class SheetCreate(LoginRequiredMixin, CreateView):
    login_url = '/auth/login/'
    model = Sheet
    form_class = SheetForm
    template_name = 'forms/form_template.html'
    # success_url = reverse_lazy('Engineering:SheetList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'اضافة شيت جديد'
        context['message'] = 'add'
        context['action_url'] = reverse_lazy('Engineering:SheetCreate')
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class=self.form_class)
        form.fields['supplier'].queryset = Supplier.objects.filter(deleted=0)
        return form

    # def get_success_url(self):
    #     messages.success(self.request, "تم اضافة شيت جديد", extra_tags="success")
    #     if self.request.POST.get('url'):
    #         return self.request.POST.get('url')
    #     else:
    #         return self.success_url

    def form_valid(self, form):
        form.save()
        obj = form.save(commit=False)
        myform = Sheet.objects.get(id=obj.id)
        myform.admin = self.request.user
        myform.save()
        # return redirect(self.get_success_url())
        return redirect('Engineering:SheetDetail', pk=obj.id)


class SheetUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = Sheet
    form_class = SheetForm
    template_name = 'forms/form_template.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل شيت: ' + str(self.object)
        context['message'] = 'update'
        context['action_url'] = reverse_lazy('Engineering:SheetUpdate', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self):
        messages.success(self.request, "تم تعديل الشيت " + str(self.object) + " بنجاح ", extra_tags="success")
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url


class SheetDelete(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = Sheet
    form_class = SheetFormDelete
    template_name = 'forms/form_template.html'

    def get_success_url(self):
        return reverse('Engineering:SheetList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'نقل الشيت الي سلة المهملات: ' + str(self.object)
        context['message'] = 'delete'
        context['action_url'] = reverse_lazy('Engineering:SheetDelete', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        messages.success(self.request, " تم نقل الشيت " + str(self.object) + ' الي سلة المهملات بنجاح ', extra_tags="success")
        myform = Sheet.objects.get(id=self.kwargs['pk'])
        myform.deleted = 1
        myform.save()
        return redirect(self.get_success_url())


class SheetRestore(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = Sheet
    form_class = SheetFormDelete
    template_name = 'forms/form_template.html'

    def get_success_url(self):
        return reverse('Engineering:SheetTrashList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'استرجاع شيت: ' + str(self.object)
        context['message'] = 'restore'
        context['action_url'] = reverse_lazy('Engineering:SheetRestore', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        messages.success(self.request, " تم استرجاع الشيت " + str(self.object) + ' الي القائمة بنجاح ', extra_tags="success")
        myform = Sheet.objects.get(id=self.kwargs['pk'])
        myform.deleted = 0
        myform.save()
        return redirect(self.get_success_url())


class SheetSuperDelete(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = Sheet
    form_class = SheetFormDelete
    template_name = 'forms/form_template.html'

    def get_success_url(self):
        return reverse('Engineering:SheetTrashList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'حذف شيت: ' + str(self.object)
        context['message'] = 'super_delete'
        context['action_url'] = reverse_lazy('Engineering:SheetSuperDelete', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        messages.success(self.request, " تم حذف الشيت " + str(self.object) + " نهائيا بنجاح ", extra_tags="success")
        my_form = Sheet.objects.get(id=self.kwargs['pk'])
        my_form.delete()
        return redirect(self.get_success_url())


def SheetDetail(request, pk):
    sheet = get_object_or_404(Sheet, id=pk)
    bons = Bon.objects.filter(sheet=sheet)
    last_bon = bons.last()
    bons_geos = bons.values_list('geo_place__name', flat=True).distinct()
    bons_comps = bons.values_list('company__name', flat=True).distinct()
    bons_cars = bons.values_list('car_number', flat=True).distinct()

    form = BonForm()
    form.fields['geo_place'].queryset = GeoPlace.objects.filter(id=-1)
    form.fields['company'].queryset = Company.objects.filter(deleted=False)
    if last_bon:
        form.fields['geo_place'].queryset = GeoPlace.objects.filter(company=last_bon.company, deleted=False)
        form.fields['car_number'].initial = last_bon.car_number
        form.fields['car_owner'].initial = last_bon.car_owner
        form.fields['kassara'].initial = last_bon.kassara
        form.fields['bon_quantity'].initial = last_bon.bon_quantity
        form.fields['bon_quantity_discount'].initial = last_bon.bon_quantity_discount
        form.fields['bon_quantity_diff'].initial = last_bon.bon_quantity_diff
        form.fields['bon_price'].initial = last_bon.bon_price
        form.fields['load_value'].initial = last_bon.load_value
        form.fields['company'].initial = last_bon.company.id
        form.fields['geo_place'].initial = last_bon.geo_place.id

    action_url = reverse_lazy('Engineering:AddSheetBon', kwargs={'pk': sheet.id})

    system_info = SystemInformation.objects.all()
    if system_info.count() > 0:
        system_info = system_info.last()
    else:
        system_info = None

    context = {
        'sheet': sheet,
        'form': form,
        'bons': bons.order_by('-id'),
        'bons_geos': bons_geos,
        'bons_comps': bons_comps,
        'bons_cars': bons_cars,
        'action_url': action_url,
        'system_info': system_info,
        'date': datetime.now().date(),
    }
    return render(request, 'Engineering/sheet_detail.html', context)


def AddSheetBon(request, pk):
    sheet = Sheet.objects.get(id=pk)
    form = BonForm(request.POST or None)
    if form.is_valid():
        bon_number = form.cleaned_data.get("bon_number")
        if bon_number in Bon.objects.filter(sheet=sheet).values_list('bon_number', flat=True):
            messages.error(request, "خطأ! رقم بون مكرر! تم إدخال سجل بنفس رقم البون مسبقا في هذا الشيت", extra_tags="danger")
        else:
            obj = form.save(commit=False)
            obj.sheet = sheet
            bon_quantity_after_discount = obj.bon_quantity - obj.bon_quantity_discount
            obj.bon_quantity_after_discount = bon_quantity_after_discount
            bon_total = obj.bon_price * obj.bon_quantity
            obj.bon_total = bon_total
            obj.geo_price = obj.geo_place.price
            obj.material_price = obj.geo_place.material_price
            material_total = obj.geo_place.material_price * obj.bon_quantity
            obj.material_total = material_total
            bon_overall = obj.geo_place.price * bon_quantity_after_discount
            obj.bon_overall = bon_overall
            supplier_value = bon_total - obj.load_value
            obj.supplier_value = supplier_value
            profit = bon_overall - (bon_total + material_total)
            obj.profit = profit
            diff_profit = obj.geo_place.material_price * obj.bon_quantity_diff
            obj.diff_profit = diff_profit
            obj.total_profit = profit + diff_profit
            obj.admin = request.user
            obj.save()
            bons = Bon.objects.filter(sheet=sheet)
            sheet.bons = bons.count()
            sheet.quantity = bons.aggregate(sum=Sum('bon_quantity')).get('sum')
            sheet.quantity_discount = bons.aggregate(sum=Sum('bon_quantity_discount')).get('sum')
            sheet.quantity_after_discount = bons.aggregate(sum=Sum('bon_quantity_after_discount')).get('sum')
            sheet.quantity_diff = bons.aggregate(sum=Sum('bon_quantity_diff')).get('sum')
            sheet.total = bons.aggregate(sum=Sum('bon_total')).get('sum')
            sheet.overall = bons.aggregate(sum=Sum('bon_overall')).get('sum')
            sheet.loads_value = bons.aggregate(sum=Sum('load_value')).get('sum')
            sheet.supplier_value = bons.aggregate(sum=Sum('supplier_value')).get('sum')
            sheet.profit = bons.aggregate(sum=Sum('total_profit')).get('sum')
            sheet.save(update_fields=['bons', 'quantity', 'quantity_discount', 'quantity_after_discount', 'quantity_diff', 'total', 'overall', 'loads_value', 'supplier_value', 'profit'])
            messages.success(request, " تم اضافة يون جديد بنجاح ", extra_tags="success")
    else:
        messages.error(request, " حدثث خطأ أثناء اضافة البون ", extra_tags="danger")
    return redirect('Engineering:SheetDetail', pk=sheet.id)


def DelSheetBon(request, pk):
    bon = Bon.objects.get(id=pk)
    sheet = bon.sheet
    bon.delete()
    bons = Bon.objects.filter(sheet=sheet)
    sheet.bons = bons.count()
    sheet.quantity = bons.aggregate(sum=Sum('bon_quantity')).get('sum')
    sheet.quantity_discount = bons.aggregate(sum=Sum('bon_quantity_discount')).get('sum')
    sheet.quantity_after_discount = bons.aggregate(sum=Sum('bon_quantity_after_discount')).get('sum')
    sheet.quantity_diff = bons.aggregate(sum=Sum('bon_quantity_diff')).get('sum')
    sheet.total = bons.aggregate(sum=Sum('bon_total')).get('sum')
    sheet.overall = bons.aggregate(sum=Sum('bon_overall')).get('sum')
    sheet.loads_value = bons.aggregate(sum=Sum('load_value')).get('sum')
    sheet.supplier_value = bons.aggregate(sum=Sum('supplier_value')).get('sum')
    sheet.profit = bons.aggregate(sum=Sum('total_profit')).get('sum')
    sheet.save(update_fields=['bons', 'quantity', 'quantity_discount', 'quantity_after_discount', 'quantity_diff', 'total', 'overall', 'loads_value', 'supplier_value', 'profit'])
    messages.success(request, " تم حذف بون بنجاح ", extra_tags="success")
    return redirect('Engineering:SheetDetail', pk=sheet.id)


def get_company_geos(request):
    if request.is_ajax():
        if request.GET.get('company_id'):
            geos = list(GeoPlace.objects.filter(company__id=int(request.GET.get('company_id')), deleted=False).values())
        else:
            geos = None
        data = {
            'geos': geos,
        }
        return JsonResponse(data)

#####################################################

def CompanySheet(request, pk):
    company = Company.objects.get(id=pk)
    bons = Bon.objects.filter(company=company, sheet__deleted=0)
    com_bons = bons.values_list('sheet__id', flat=True).distinct()
    sheets = Sheet.objects.filter(id__in=com_bons, deleted=0)
    return render(request, 'Engineering/More/company_sheet.html', {
        'company': company,
        'company_sheet': sheets.order_by('-id'),
        'company_bons': bons.count(),
        'company_quantity': sheets.aggregate(sum=Sum('quantity')).get('sum'),
        'company_quantity_discount': sheets.aggregate(sum=Sum('quantity_discount')).get('sum'),
        'company_quantity_after_discount': sheets.aggregate(sum=Sum('quantity_after_discount')).get('sum'),
        'company_prices': sheets.aggregate(sum=Sum('overall')).get('sum'),
    })


def GeoSheet(request, pk):
    geo = GeoPlace.objects.get(id=pk)
    bons = Bon.objects.filter(geo_place=geo, sheet__deleted=0)
    geo_bons = bons.values_list('sheet__id', flat=True).distinct()
    sheets = Sheet.objects.filter(id__in=geo_bons, deleted=0)
    return render(request, 'Engineering/More/geo_sheet.html', {
        'geo': geo,
        'geo_sheet': sheets.order_by('-id'),
        'geo_bons': bons.count(),
        'geo_quantity': sheets.aggregate(sum=Sum('quantity')).get('sum'),
        'geo_quantity_discount': sheets.aggregate(sum=Sum('quantity_discount')).get('sum'),
        'geo_quantity_after_discount': sheets.aggregate(sum=Sum('quantity_after_discount')).get('sum'),
        'geo_prices': sheets.aggregate(sum=Sum('overall')).get('sum'),
    })


def SupplierSheet(request, pk):
    supplier = Supplier.objects.get(id=pk)
    sheets = Sheet.objects.filter(supplier=supplier, deleted=0)
    return render(request, 'Engineering/More/supplier_sheet.html', {
        'supplier': supplier,
        'supplier_sheet': sheets.order_by('-id'),
        'supplier_bons': sheets.aggregate(sum=Sum('bons')).get('sum'),
        'supplier_quantity': sheets.aggregate(sum=Sum('quantity')).get('sum'),
        'supplier_prices': sheets.aggregate(sum=Sum('total')).get('sum'),
        'supplier_loads': sheets.aggregate(sum=Sum('loads_value')).get('sum'),
    })


def CompanyBon(request, pk):
    company = Company.objects.get(id=pk)
    bons = Bon.objects.filter(company=company, sheet__deleted=0)
    com_bons = bons.values_list('sheet__id', flat=True).distinct()
    sheets = Sheet.objects.filter(id__in=com_bons, deleted=0)
    return render(request, 'Engineering/More/company_bon.html', {
        'company': company,
        'company_sheet': sheets.count(),
        'company_bon': bons.order_by('-id'),
        'company_quantity': sheets.aggregate(sum=Sum('quantity')).get('sum'),
        'company_quantity_discount': sheets.aggregate(sum=Sum('quantity_discount')).get('sum'),
        'company_quantity_after_discount': sheets.aggregate(sum=Sum('quantity_after_discount')).get('sum'),
        'company_prices': sheets.aggregate(sum=Sum('overall')).get('sum'),
    })


def GeoBon(request, pk):
    geo = GeoPlace.objects.get(id=pk)
    bons = Bon.objects.filter(geo_place=geo, sheet__deleted=0)
    geo_bons = bons.values_list('sheet__id', flat=True).distinct()
    sheets = Sheet.objects.filter(id__in=geo_bons, deleted=0)
    return render(request, 'Engineering/More/geo_bon.html', {
        'geo': geo,
        'geo_sheet': sheets.count(),
        'geo_bon': bons.order_by('-id'),
        'geo_quantity': sheets.aggregate(sum=Sum('quantity')).get('sum'),
        'geo_quantity_discount': sheets.aggregate(sum=Sum('quantity_discount')).get('sum'),
        'geo_quantity_after_discount': sheets.aggregate(sum=Sum('quantity_after_discount')).get('sum'),
        'geo_prices': sheets.aggregate(sum=Sum('overall')).get('sum'),
    })


def SupplierBon(request, pk):
    supplier = Supplier.objects.get(id=pk)
    sheets = Sheet.objects.filter(supplier=supplier, deleted=0)
    return render(request, 'Engineering/More/supplier_bon.html', {
        'supplier': supplier,
        'supplier_sheet': sheets.count(),
        'supplier_bon': Bon.objects.filter(sheet__supplier=supplier, sheet__deleted=0).order_by('-id'),
        'supplier_bons': sheets.aggregate(sum=Sum('bons')).get('sum'),
        'supplier_quantity': sheets.aggregate(sum=Sum('quantity')).get('sum'),
        'supplier_prices': sheets.aggregate(sum=Sum('total')).get('sum'),
        'supplier_loads': sheets.aggregate(sum=Sum('loads_value')).get('sum'),
    })


def CompanyProfit(request, pk):
    company = Company.objects.get(id=pk)
    bons = Bon.objects.filter(company=company, sheet__deleted=0)
    com_bons = bons.values_list('sheet__id', flat=True).distinct()
    sheets = Sheet.objects.filter(id__in=com_bons, deleted=0)
    return render(request, 'Engineering/More/company_profit.html', {
        'company': company,
        'company_bons': bons.count(),
        'company_profit': sheets.aggregate(sum=Sum('profit')).get('sum'),
        'company_quantity': bons.aggregate(sum=Sum('bon_quantity')).get('sum'),
        'company_prices': bons.aggregate(sum=Sum('supplier_value')).get('sum'),
        'company_total': bons.aggregate(sum=Sum('bon_overall')).get('sum'),
        'company_months_profit': bons.values('date__year', 'date__month').annotate(
            bons=Count('id'),
            quantity=Sum('bon_quantity'),
            quantity_discount=Sum('bon_quantity_discount'),
            quantity_after_discount=Sum('bon_quantity_after_discount'),
            total=Sum('supplier_value'),
            profit=Sum('total_profit'),
            overall=Sum('bon_overall'),
        ).order_by('-date__year', '-date__month')
    })


def GeoProfit(request, pk):
    geo = GeoPlace.objects.get(id=pk)
    bons = Bon.objects.filter(geo_place=geo, sheet__deleted=0)
    com_bons = bons.values_list('sheet__id', flat=True).distinct()
    sheets = Sheet.objects.filter(id__in=com_bons, deleted=0)
    return render(request, 'Engineering/More/geo_profit.html', {
        'geo': geo,
        'geo_bons': bons.count(),
        'geo_profit': sheets.aggregate(sum=Sum('profit')).get('sum'),
        'geo_quantity': bons.aggregate(sum=Sum('bon_quantity')).get('sum'),
        'geo_prices': bons.aggregate(sum=Sum('supplier_value')).get('sum'),
        'geo_total': bons.aggregate(sum=Sum('bon_overall')).get('sum'),
        'geo_months_profit': bons.values('date__year', 'date__month').annotate(
            bons=Count('id'),
            quantity=Sum('bon_quantity'),
            quantity_discount=Sum('bon_quantity_discount'),
            quantity_after_discount=Sum('bon_quantity_after_discount'),
            total=Sum('supplier_value'),
            profit=Sum('total_profit'),
            overall=Sum('bon_overall'),
        ).order_by('-date__year', '-date__month')
    })


def SupplierProfit(request, pk):
    supplier = Supplier.objects.get(id=pk)
    sheets = Sheet.objects.filter(supplier=supplier, deleted=0)
    bons = Bon.objects.filter(sheet__supplier=supplier, sheet__deleted=0)
    return render(request, 'Engineering/More/supplier_profit.html', {
        'supplier': supplier,
        'supplier_bons': bons.count(),
        'supplier_profit': sheets.aggregate(sum=Sum('profit')).get('sum'),
        'supplier_quantity': bons.aggregate(sum=Sum('bon_quantity')).get('sum'),
        'supplier_prices': bons.aggregate(sum=Sum('supplier_value')).get('sum'),
        'supplier_total': bons.aggregate(sum=Sum('bon_overall')).get('sum'),
        'supplier_months_profit': bons.values('date__year', 'date__month').annotate(
            bons=Count('id'),
            quantity=Sum('bon_quantity'),
            total=Sum('supplier_value'),
            profit=Sum('total_profit'),
            overall=Sum('bon_overall'),
        ).order_by('-date__year', '-date__month')
    })


def MonthsProfit(request):
    supplier_pays = SupplierPayment.objects.all()
    supplier_payment_sum = supplier_pays.aggregate(price=Sum('cash_amount')).get('price')
    supplier_total_account = Sheet.objects.filter(deleted=0).aggregate(total=Sum('total')).get('total')
    supplier_loads_account = Sheet.objects.filter(deleted=0).aggregate(total=Sum('loads_value')).get('total')

    if supplier_payment_sum:
        supplier_payment_sum = supplier_payment_sum
    else:
        supplier_payment_sum = 0

    if supplier_total_account:
        supplier_total_account = supplier_total_account
    else:
        supplier_total_account = 0

    if supplier_loads_account:
        supplier_loads_account = supplier_loads_account
    else:
        supplier_loads_account = 0

    suppliers_all_pays = supplier_payment_sum + supplier_loads_account
    suppliers_total = supplier_total_account - suppliers_all_pays

    ##########################

    company_pays = CompanyPayment.objects.all()
    company_payment_sum = company_pays.aggregate(price=Sum('cash_amount')).get('price')
    company_total_account = Sheet.objects.filter(deleted=0).aggregate(overall=Sum('overall')).get('overall')

    if company_payment_sum:
        company_payment_sum = company_payment_sum
    else:
        company_payment_sum = 0

    if company_total_account:
        company_total_account = company_total_account
    else:
        company_total_account = 0

    companies_total = company_total_account - company_payment_sum

    ##########################

    months_profit = Bon.objects.filter(sheet__deleted=0).values('date__year', 'date__month').annotate(
        bons=Count('id'),
        quantity=Sum('bon_quantity'),
        quantity_discount=Sum('bon_quantity_discount'),
        quantity_after_discount=Sum('bon_quantity_after_discount'),
        total=Sum('supplier_value'),
        profit=Sum('total_profit'),
        overall=Sum('bon_overall'),
    ).order_by('-date__year', '-date__month')

    all_profit = Bon.objects.filter(sheet__deleted=0).aggregate(
        bons=Count('id'),
        quantity=Sum('bon_quantity'),
        quantity_discount=Sum('bon_quantity_discount'),
        quantity_after_discount=Sum('bon_quantity_after_discount'),
        total=Sum('supplier_value'),
        profit=Sum('total_profit'),
        overall=Sum('bon_overall'),
    )

    months_name = [""]
    months_val = [0]
    all_months = Bon.objects.filter(sheet__deleted=0).values('date__year', 'date__month').order_by('-date__year', '-date__month')
    if all_months.count() > 12:
        all_months = all_months.annotate(sum=Sum('total_profit'))[:12]
    else:
        all_months = all_months.annotate(sum=Sum('total_profit'))[:all_months.count()]
    for item in all_months:
        if item['date__month'] == 1:
            months_name.insert(1, 'يناير' + str(item['date__year']))
        elif item['date__month'] == 2:
            months_name.insert(1, 'فبراير' + str(item['date__year']))
        elif item['date__month'] == 3:
            months_name.insert(1, 'مارس' + str(item['date__year']))
        elif item['date__month'] == 4:
            months_name.insert(1, 'أبريل' + str(item['date__year']))
        elif item['date__month'] == 5:
            months_name.insert(1, 'مايو' + str(item['date__year']))
        elif item['date__month'] == 6:
            months_name.insert(1, 'يونيو' + str(item['date__year']))
        elif item['date__month'] == 7:
            months_name.insert(1, 'يوليو' + str(item['date__year']))
        elif item['date__month'] == 8:
            months_name.insert(1, 'أغسطس' + str(item['date__year']))
        elif item['date__month'] == 9:
            months_name.insert(1, 'سبتمبر' + str(item['date__year']))
        elif item['date__month'] == 10:
            months_name.insert(1, 'أكتوبر' + str(item['date__year']))
        elif item['date__month'] == 11:
            months_name.insert(1, 'نوفمبر' + str(item['date__year']))
        elif item['date__month'] == 12:
            months_name.insert(1, 'ديسمبر' + str(item['date__year']))
        months_val.insert(1, item['sum'])

    return render(request, 'Engineering/months_profit.html', {
        'months_profit': months_profit,
        'all_profit': all_profit,
        'months_name': months_name,
        'months_val': months_val,
        'suppliers_all_pays': suppliers_all_pays,
        'supplier_total_account': supplier_total_account,
        'suppliers_total': suppliers_total,
        'company_payment_sum': company_payment_sum,
        'company_total_account': company_total_account,
        'companies_total': companies_total,
    })


# Supplier payment list
class SupplierPayments(LoginRequiredMixin, DetailView):
    login_url = '/auth/login/'
    model = Supplier
    template_name = 'Engineering/Payment/supplier_payment.html'

    def get_context_data(self, **kwargs):
        queryset = SupplierPayment.objects.filter(supplier=self.object)
        payment_sum = queryset.aggregate(price=Sum('cash_amount')).get('price')
        total_account = Sheet.objects.filter(supplier=self.object, deleted=0).aggregate(total=Sum('total')).get('total')
        loads_account = Sheet.objects.filter(supplier=self.object, deleted=0).aggregate(total=Sum('loads_value')).get('total')

        if payment_sum:
            payment_sum = payment_sum
        else:
            payment_sum = 0

        if total_account:
            total_account = total_account
        else:
            total_account = 0

        if loads_account:
            loads_account = loads_account
        else:
            loads_account = 0

        account = total_account - loads_account
        total = account - payment_sum

        context = super().get_context_data(**kwargs)
        context['payment'] = queryset.order_by('-id')
        context['payment_sum'] = payment_sum
        context['account'] = account
        context['total'] = total
        context['title'] = 'مسحوبات المورد: ' + str(self.object)
        form = SupplierPaymentForm(self.request.POST or None)
        form.fields['cash_amount'].initial = 1
        context['form'] = form
        context['type'] = 'list'
        context['supplier'] = self.object
        return context


# Supplier payment list_div
class SupplierPayments_div(LoginRequiredMixin, DetailView):
    login_url = '/auth/login/'
    model = Supplier
    template_name = 'Engineering/Payment/supplier_payment_div.html'

    def get_context_data(self, **kwargs):
        queryset = SupplierPayment.objects.filter(supplier=self.object)
        payment_sum = queryset.aggregate(price=Sum('cash_amount')).get('price')
        total_account = Sheet.objects.filter(supplier=self.object, deleted=0).aggregate(total=Sum('total')).get('total')
        loads_account = Sheet.objects.filter(supplier=self.object, deleted=0).aggregate(total=Sum('loads_value')).get('total')

        if payment_sum:
            payment_sum = payment_sum
        else:
            payment_sum = 0

        if total_account:
            total_account = total_account
        else:
            total_account = 0

        if loads_account:
            loads_account = loads_account
        else:
            loads_account = 0

        account = total_account - loads_account
        total = account - payment_sum

        context = super().get_context_data(**kwargs)
        context['payment'] = queryset.order_by('-id')
        context['payment_sum'] = payment_sum
        context['account'] = account
        context['total'] = total
        context['title'] = 'مسحوبات المورد: ' + str(self.object)
        form = SupplierPaymentForm(self.request.POST or None)
        form.fields['cash_amount'].initial = 1
        context['form'] = form
        context['type'] = 'list'
        context['supplier'] = self.object
        return context


# create supplier payment function
def SupplierPaymentCreate(request):
    if request.is_ajax():
        supplier_id = request.POST.get('id')
        supplier = Supplier.objects.get(id=supplier_id)

        payment_date = request.POST.get('payment_date')
        cash_amount = request.POST.get('cash_amount')
        desc = request.POST.get('desc')


        if supplier and payment_date and cash_amount:
            obj = SupplierPayment()
            obj.supplier = supplier
            obj.payment_date = payment_date
            obj.admin = request.user
            obj.cash_amount = cash_amount
            obj.desc = desc
            obj.save()

            if obj:
                response = {
                    'msg': 1
                }
        else:
            response = {
                'msg': 0
            }
        return JsonResponse(response)


# delete supplier payment item
def SupplierPaymentDelete(request):
    if request.is_ajax():
        payment_id = request.POST.get('payment_id')
        obj = SupplierPayment.objects.get(id=payment_id)
        obj.delete()

        if obj:
            response = {
                'msg': 'Send Successfully'
            }
        else:
            response = {
                'msg': 'خطأ'
            }

        return JsonResponse(response)



# Supplier payment list
class CompanyPayments(LoginRequiredMixin, DetailView):
    login_url = '/auth/login/'
    model = Company
    template_name = 'Engineering/Payment/company_payment.html'

    def get_context_data(self, **kwargs):
        queryset = CompanyPayment.objects.filter(company=self.object)
        payment_sum = queryset.aggregate(price=Sum('cash_amount')).get('price')
        total_account = Bon.objects.filter(company=self.object, sheet__deleted=0).aggregate(total=Sum('bon_overall')).get('total')

        if payment_sum:
            payment_sum = payment_sum
        else:
            payment_sum = 0

        if total_account:
            total_account = total_account
        else:
            total_account = 0

        total = total_account - payment_sum

        context = super().get_context_data(**kwargs)
        context['payment'] = queryset.order_by('-id')
        context['payment_sum'] = payment_sum
        context['total_account'] = total_account
        context['total'] = total
        context['title'] = 'مسحوباتي من الشركة: ' + str(self.object)
        form = CompanyPaymentForm(self.request.POST or None)
        form.fields['cash_amount'].initial = 1
        context['form'] = form
        context['type'] = 'list'
        context['company'] = self.object
        context['geos'] = GeoPlace.objects.filter(company=self.object)
        return context

# Company_div payment list
class CompanyPayments_div(LoginRequiredMixin, DetailView):
    login_url = '/auth/login/'
    model = Company
    template_name = 'Engineering/Payment/company_payment_div.html'

    def get_context_data(self, **kwargs):
        queryset = CompanyPayment.objects.filter(company=self.object)
        payment_sum = queryset.aggregate(price=Sum('cash_amount')).get('price')
        total_account = Bon.objects.filter(company=self.object, sheet__deleted=0).aggregate(total=Sum('bon_overall')).get('total')

        if payment_sum:
            payment_sum = payment_sum
        else:
            payment_sum = 0

        if total_account:
            total_account = total_account
        else:
            total_account = 0

        total = total_account - payment_sum

        context = super().get_context_data(**kwargs)
        context['payment'] = queryset.order_by('-id')
        context['payment_sum'] = payment_sum
        context['total_account'] = total_account
        context['total'] = total
        context['title'] = 'مسحوباتي من الشركة: ' + str(self.object)
        form = CompanyPaymentForm(self.request.POST or None)
        form.fields['cash_amount'].initial = 1
        context['form'] = form
        context['type'] = 'list'
        context['company'] = self.object
        context['geos'] = GeoPlace.objects.filter(company=self.object)
        return context

# create compnay payment function
def CompanyPaymentCreate(request):
    if request.is_ajax():
        company_id = request.POST.get('id')
        company = Company.objects.get(id=company_id)

        payment_date = request.POST.get('payment_date')
        cash_amount = request.POST.get('cash_amount')
        geo_place = request.POST.get('geo_place')
        desc = request.POST.get('desc')

        if company and payment_date and cash_amount:
            obj = CompanyPayment()
            obj.company = company
            obj.payment_date = payment_date
            obj.admin = request.user
            obj.cash_amount = cash_amount
            if geo_place:
                obj.geo_place = GeoPlace.objects.get(id=int(geo_place))
            else:
                obj.geo_place = None
            obj.desc = desc
            obj.save()

            if obj:
                response = {
                    'msg': 1
                }
        else:
            response = {
                'msg': 0
            }
        return JsonResponse(response)


# delete supplier payment item
def CompanyPaymentDelete(request):
    if request.is_ajax():
        payment_id = request.POST.get('payment_id')
        obj = CompanyPayment.objects.get(id=payment_id)
        obj.delete()

        if obj:
            response = {
                'msg': 'Send Successfully'
            }
        else:
            response = {
                'msg': 'خطأ'
            }

        return JsonResponse(response)


def BonsReports(request):
    bons = Bon.objects.filter(sheet__deleted=0)
    bons_sups = bons.values_list('sheet__supplier__name', flat=True).distinct()
    bons_geos = bons.values_list('geo_place__name', flat=True).distinct()
    bons_comps = bons.values_list('company__name', flat=True).distinct()
    bons_cars = bons.values_list('car_number', flat=True).distinct()

    system_info = SystemInformation.objects.all()
    if system_info.count() > 0:
        system_info = system_info.last()
    else:
        system_info = None

    context = {
        'bons': bons.order_by('-id'),
        'bons_sups': bons_sups,
        'bons_geos': bons_geos,
        'bons_comps': bons_comps,
        'bons_cars': bons_cars,
        'system_info': system_info,
        'date': datetime.now().date(),
    }
    return render(request, 'Engineering/bons_reports.html', context)


def SupplierReport(request, pk):
    # form to filter data from ... to....
    filter_form = SupplierReoprtForm

    if request.GET.get('submit'):
        print('success')
        # get supplier object
        supplier = get_object_or_404(Supplier, id=pk)
        # get payment for supplier

        if request.GET.get('from_date') and request.GET.get('to_date'):
            payment = SupplierPayment.objects.filter(created_date__range=[request.GET.get('from_date'), request.GET.get('to_date')]).order_by('-id')

        if request.GET.get('from_date') and request.GET.get('to_date'):
            bons = Bon.objects.filter(sheet__supplier=supplier, date__range=[request.GET.get('from_date'), request.GET.get('to_date')])

        bons_count = bons.count()
        total_quantity = bons.aggregate(sum=Sum('bon_quantity')).get('sum')

        payment_sum = payment.aggregate(sum=Sum('cash_amount')).get('sum')
        if payment_sum:
            payment_sum = payment_sum
        else:
            payment_sum = 0

        supplier_total_payment = bons.aggregate(sum=Sum('supplier_value')).get('sum')
        if supplier_total_payment:
            supplier_total_payment = supplier_total_payment
        else:
            supplier_total_payment = 0

        if payment_sum:
            total_supplier_account = supplier_total_payment - payment_sum
        else:
            total_supplier_account = supplier_total_payment
        total_load_value = bons.aggregate(sum=Sum('load_value')).get('sum')
    else:
        supplier = supplier = get_object_or_404(Supplier, id=pk)
        payment = None
        bons_count = 0
        total_quantity = 0
        payment_sum = 0
        date_from = None
        date_to = None
        total_supplier_account = 0
        supplier_total_payment = 0
        total_load_value = 0
    context = {
        'form': filter_form,
        'supplier': supplier,
        'payment': payment,
        'supplier_bon_count': bons_count,
        'supplier_quantity': total_quantity,
        'payment_sum': payment_sum,
        'date_from': request.GET.get('from_date'),
        'date_to': request.GET.get('to_date'),
        'total_supplier_account': total_supplier_account,
        'supplier_total_payment': supplier_total_payment,
        'total_load_value': total_load_value


    }
    return render(request, 'Engineering/reports/supplier_report.html', context)