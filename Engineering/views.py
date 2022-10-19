import datetime
from django.db.models.aggregates import Sum, Count
from django.http import HttpResponse
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
    template_name = 'Engineering/More/geoplace_price_history.html'

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
    success_url = reverse_lazy('Engineering:SheetList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'اضافة شيت جديد'
        context['message'] = 'add'
        context['action_url'] = reverse_lazy('Engineering:SheetCreate')
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class=self.form_class)
        form.fields['company'].queryset = Company.objects.filter(deleted=0, active=True)
        form.fields['supplier'].queryset = Supplier.objects.filter(deleted=0)
        return form

    def get_success_url(self):
        messages.success(self.request, "تم اضافة شيت جديد", extra_tags="success")
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url

    def form_valid(self, form):
        form.save()
        obj = form.save(commit=False)
        myform = Sheet.objects.get(id=obj.id)
        myform.admin = self.request.user
        myform.save()
        return redirect(self.get_success_url())


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
    bons_geos = bons.values_list('geo_place__name', flat=True).distinct()

    form = BonForm()
    form.fields['geo_place'].queryset = GeoPlace.objects.filter(company=sheet.company, deleted=False)

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
        'action_url': action_url,
        'system_info': system_info,
        'date': datetime.now().date(),
    }
    return render(request, 'Engineering/sheet_detail.html', context)


def AddSheetBon(request, pk):
    sheet = Sheet.objects.get(id=pk)
    form = BonForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.sheet = sheet
        obj.bon_total = obj.bon_price * obj.bon_quantity
        obj.geo_price = obj.geo_place.price
        obj.bon_overall = obj.geo_place.price * obj.bon_quantity
        obj.profit = obj.geo_place.price - obj.bon_price
        obj.total_profit = (obj.geo_place.price - obj.bon_price) * obj.bon_quantity
        obj.admin = request.user
        obj.save()
        sheet.profit = Bon.objects.filter(sheet=sheet).aggregate(sum=Sum('total_profit')).get('sum')
        sheet.save(update_fields=['profit'])
        messages.success(request, " تم اضافة يون جديد بنجاح ", extra_tags="success")
    else:
        messages.error(request, " حدثث خطأ أثناء اضافة البون ", extra_tags="danger")
    return redirect('Engineering:SheetDetail', pk=sheet.id)


def DelSheetBon(request, pk):
    bon = Bon.objects.get(id=pk)
    sheet = bon.sheet
    bon.delete()
    sheet.profit = Bon.objects.filter(sheet=sheet).aggregate(sum=Sum('total_profit')).get('sum')
    sheet.save(update_fields=['profit'])
    messages.success(request, " تم حذف بون بنجاح ", extra_tags="success")
    return redirect('Engineering:SheetDetail', pk=sheet.id)


#####################################################

class CompanySheet(LoginRequiredMixin, DetailView):
    login_url = '/auth/login/'
    model = Sheet
    template_name = 'Engineering/More/company_sheet.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company_sheet'] = self.model.objects.filter(company__id=self.kwargs['pk'], deleted=0).order_by('-id')
        context['company_sheet_bons'] = Bon.objects.filter(sheet__company__id=self.kwargs['pk'], sheet__deleted=0).count()
        context['company'] = get_object_or_404(Company, id=self.kwargs['pk'])
        context['company_profit'] = self.model.objects.filter(company__id=self.kwargs['pk'], deleted=0).aggregate(sum=Sum('profit')).get('sum')
        context['company_quantity'] = Bon.objects.filter(sheet__company__id=self.kwargs['pk'], sheet__deleted=0).aggregate(sum=Sum('bon_quantity')).get('sum')
        context['company_prices'] = Bon.objects.filter(sheet__company__id=self.kwargs['pk'], sheet__deleted=0).aggregate(sum=Sum('bon_total')).get('sum')
        context['company_total'] = Bon.objects.filter(sheet__company__id=self.kwargs['pk'], sheet__deleted=0).aggregate(sum=Sum('bon_overall')).get('sum')
        return context


class GeoSheet(LoginRequiredMixin, DetailView):
    login_url = '/auth/login/'
    model = Sheet
    template_name = 'Engineering/More/geo_sheet.html'

    def get_context_data(self, **kwargs):
        bons_sheets = Bon.objects.filter(geo_place__id=self.kwargs['pk'], sheet__deleted=0).values_list('sheet__id', flat=True).distinct()
        context = super().get_context_data(**kwargs)
        context['geo'] = get_object_or_404(GeoPlace, id=self.kwargs['pk'])
        context['geo_sheet'] = self.model.objects.filter(id__in=bons_sheets, deleted=0).order_by('-id')
        context['geo_sheet_bons'] = Bon.objects.filter(geo_place__id=self.kwargs['pk'], sheet__deleted=0).count()
        context['geo_profit'] = Bon.objects.filter(geo_place__id=self.kwargs['pk'], sheet__deleted=0).aggregate(sum=Sum('total_profit')).get('sum')
        context['geo_quantity'] = Bon.objects.filter(geo_place__id=self.kwargs['pk'], sheet__deleted=0).aggregate(sum=Sum('bon_quantity')).get('sum')
        context['geo_prices'] = Bon.objects.filter(geo_place__id=self.kwargs['pk'], sheet__deleted=0).aggregate(sum=Sum('bon_total')).get('sum')
        context['geo_total'] = Bon.objects.filter(geo_place__id=self.kwargs['pk'], sheet__deleted=0).aggregate(sum=Sum('bon_overall')).get('sum')
        return context


class SupplierSheet(LoginRequiredMixin, DetailView):
    login_url = '/auth/login/'
    model = Sheet
    template_name = 'Engineering/More/supplier_sheet.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['supplier'] = get_object_or_404(Supplier, id=self.kwargs['pk'])
        context['supplier_sheet'] = self.model.objects.filter(supplier__id=self.kwargs['pk'], deleted=0).order_by('-id')
        context['supplier_sheet_bons'] = Bon.objects.filter(sheet__supplier__id=self.kwargs['pk'], sheet__deleted=0).count()
        context['supplier_profit'] = self.model.objects.filter(supplier__id=self.kwargs['pk'], deleted=0).aggregate(sum=Sum('profit')).get('sum')
        context['supplier_quantity'] = Bon.objects.filter(sheet__supplier__id=self.kwargs['pk'], sheet__deleted=0).aggregate(sum=Sum('bon_quantity')).get('sum')
        context['supplier_prices'] = Bon.objects.filter(sheet__supplier__id=self.kwargs['pk'], sheet__deleted=0).aggregate(sum=Sum('bon_total')).get('sum')
        context['supplier_total'] = Bon.objects.filter(sheet__supplier__id=self.kwargs['pk'], sheet__deleted=0).aggregate(sum=Sum('bon_overall')).get('sum')
        return context


class CompanyBon(LoginRequiredMixin, DetailView):
    login_url = '/auth/login/'
    model = Sheet
    template_name = 'Engineering/More/company_bon.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company_bon'] = Bon.objects.filter(sheet__company__id=self.kwargs['pk'], sheet__deleted=0).order_by('-id')
        context['company_bon_sheets'] = self.model.objects.filter(company__id=self.kwargs['pk'], deleted=0).count()
        context['company'] = get_object_or_404(Company, id=self.kwargs['pk'])
        context['company_profit'] = Bon.objects.filter(sheet__company__id=self.kwargs['pk'], sheet__deleted=0).aggregate(sum=Sum('total_profit')).get('sum')
        context['company_quantity'] = Bon.objects.filter(sheet__company__id=self.kwargs['pk'], sheet__deleted=0).aggregate(sum=Sum('bon_quantity')).get('sum')
        context['company_prices'] = Bon.objects.filter(sheet__company__id=self.kwargs['pk'], sheet__deleted=0).aggregate(sum=Sum('bon_total')).get('sum')
        context['company_total'] = Bon.objects.filter(sheet__company__id=self.kwargs['pk'], sheet__deleted=0).aggregate(sum=Sum('bon_overall')).get('sum')
        return context


class GeoBon(LoginRequiredMixin, DetailView):
    login_url = '/auth/login/'
    model = Sheet
    template_name = 'Engineering/More/geo_bon.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['geo'] = get_object_or_404(GeoPlace, id=self.kwargs['pk'])
        context['geo_bon'] = Bon.objects.filter(geo_place__id=self.kwargs['pk'], sheet__deleted=0).order_by('-id')
        context['geo_bon_sheets'] = Bon.objects.filter(geo_place__id=self.kwargs['pk'], sheet__deleted=0).values('sheet__id').distinct().count()
        context['geo_profit'] = Bon.objects.filter(geo_place__id=self.kwargs['pk'], sheet__deleted=0).aggregate(sum=Sum('total_profit')).get('sum')
        context['geo_quantity'] = Bon.objects.filter(geo_place__id=self.kwargs['pk'], sheet__deleted=0).aggregate(sum=Sum('bon_quantity')).get('sum')
        context['geo_prices'] = Bon.objects.filter(geo_place__id=self.kwargs['pk'], sheet__deleted=0).aggregate(sum=Sum('bon_total')).get('sum')
        context['geo_total'] = Bon.objects.filter(geo_place__id=self.kwargs['pk'], sheet__deleted=0).aggregate(sum=Sum('bon_overall')).get('sum')
        return context


class SupplierBon(LoginRequiredMixin, DetailView):
    login_url = '/auth/login/'
    model = Sheet
    template_name = 'Engineering/More/supplier_bon.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['supplier_bon'] = Bon.objects.filter(sheet__supplier__id=self.kwargs['pk'], sheet__deleted=0).order_by('-id')
        context['supplier_bon_sheets'] = self.model.objects.filter(supplier__id=self.kwargs['pk'], deleted=0).count()
        context['supplier'] = get_object_or_404(Supplier, id=self.kwargs['pk'])
        context['supplier_profit'] = Bon.objects.filter(sheet__supplier__id=self.kwargs['pk'], sheet__deleted=0).aggregate(sum=Sum('total_profit')).get('sum')
        context['supplier_quantity'] = Bon.objects.filter(sheet__supplier__id=self.kwargs['pk'], sheet__deleted=0).aggregate(sum=Sum('bon_quantity')).get('sum')
        context['supplier_prices'] = Bon.objects.filter(sheet__supplier__id=self.kwargs['pk'], sheet__deleted=0).aggregate(sum=Sum('bon_total')).get('sum')
        context['supplier_total'] = Bon.objects.filter(sheet__supplier__id=self.kwargs['pk'], sheet__deleted=0).aggregate(sum=Sum('bon_overall')).get('sum')
        return context


class CompanyProfit(LoginRequiredMixin, DetailView):
    login_url = '/auth/login/'
    model = Sheet
    template_name = 'Engineering/More/company_profit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company_sheet_bons'] = Bon.objects.filter(sheet__company__id=self.kwargs['pk'], sheet__deleted=0).count()
        context['company'] = get_object_or_404(Company, id=self.kwargs['pk'])
        context['company_profit'] = self.model.objects.filter(company__id=self.kwargs['pk'], deleted=0).aggregate(sum=Sum('profit')).get('sum')
        context['company_quantity'] = Bon.objects.filter(sheet__company__id=self.kwargs['pk'], sheet__deleted=0).aggregate(sum=Sum('bon_quantity')).get('sum')
        context['company_prices'] = Bon.objects.filter(sheet__company__id=self.kwargs['pk'], sheet__deleted=0).aggregate(sum=Sum('bon_total')).get('sum')
        context['company_total'] = Bon.objects.filter(sheet__company__id=self.kwargs['pk'], sheet__deleted=0).aggregate(sum=Sum('bon_overall')).get('sum')

        context['company_months_profit'] = Bon.objects.filter(sheet__company__id=self.kwargs['pk'], sheet__deleted=0).values('date__year', 'date__month').annotate(
            bons=Count('id'),
            quantity=Sum('bon_quantity'),
            total=Sum('bon_total'),
            profit=Sum('total_profit'),
            overall=Sum('bon_overall'),
        ).order_by('-date__year', '-date__month')

        return context


class GeoProfit(LoginRequiredMixin, DetailView):
    login_url = '/auth/login/'
    model = Sheet
    template_name = 'Engineering/More/geo_profit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['geo'] = get_object_or_404(GeoPlace, id=self.kwargs['pk'])
        context['geo_sheet_bons'] = Bon.objects.filter(geo_place__id=self.kwargs['pk'], sheet__deleted=0).count()
        context['geo_profit'] = Bon.objects.filter(geo_place__id=self.kwargs['pk'], sheet__deleted=0).aggregate(sum=Sum('total_profit')).get('sum')
        context['geo_quantity'] = Bon.objects.filter(geo_place__id=self.kwargs['pk'], sheet__deleted=0).aggregate(sum=Sum('bon_quantity')).get('sum')
        context['geo_prices'] = Bon.objects.filter(geo_place__id=self.kwargs['pk'], sheet__deleted=0).aggregate(sum=Sum('bon_total')).get('sum')
        context['geo_total'] = Bon.objects.filter(geo_place__id=self.kwargs['pk'], sheet__deleted=0).aggregate(sum=Sum('bon_overall')).get('sum')

        context['geo_months_profit'] = Bon.objects.filter(geo_place__id=self.kwargs['pk'], sheet__deleted=0).values('date__year', 'date__month').annotate(
            bons=Count('id'),
            quantity=Sum('bon_quantity'),
            total=Sum('bon_total'),
            profit=Sum('total_profit'),
            overall=Sum('bon_overall'),
        ).order_by('-date__year', '-date__month')

        return context


class SupplierProfit(LoginRequiredMixin, DetailView):
    login_url = '/auth/login/'
    model = Sheet
    template_name = 'Engineering/More/supplier_profit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['supplier'] = get_object_or_404(Supplier, id=self.kwargs['pk'])
        context['supplier_sheet_bons'] = Bon.objects.filter(sheet__supplier__id=self.kwargs['pk'], sheet__deleted=0).count()
        context['supplier_profit'] = self.model.objects.filter(supplier__id=self.kwargs['pk'], deleted=0).aggregate(sum=Sum('profit')).get('sum')
        context['supplier_quantity'] = Bon.objects.filter(sheet__supplier__id=self.kwargs['pk'], sheet__deleted=0).aggregate(sum=Sum('bon_quantity')).get('sum')
        context['supplier_prices'] = Bon.objects.filter(sheet__supplier__id=self.kwargs['pk'], sheet__deleted=0).aggregate(sum=Sum('bon_total')).get('sum')
        context['supplier_total'] = Bon.objects.filter(sheet__supplier__id=self.kwargs['pk'], sheet__deleted=0).aggregate(sum=Sum('bon_overall')).get('sum')

        context['supplier_months_profit'] = Bon.objects.filter(sheet__supplier__id=self.kwargs['pk'], sheet__deleted=0).values('date__year', 'date__month').annotate(
            bons=Count('id'),
            quantity=Sum('bon_quantity'),
            total=Sum('bon_total'),
            profit=Sum('total_profit'),
            overall=Sum('bon_overall'),
        ).order_by('-date__year', '-date__month')

        return context


def MonthsProfit(request):
    months_profit = Bon.objects.filter(sheet__deleted=0).values('date__year', 'date__month').annotate(
        bons=Count('id'),
        quantity=Sum('bon_quantity'),
        total=Sum('bon_total'),
        profit=Sum('total_profit'),
        overall=Sum('bon_overall'),
    ).order_by('-date__year', '-date__month')

    all_profit = Bon.objects.filter(sheet__deleted=0).aggregate(
        bons=Count('id'),
        quantity=Sum('bon_quantity'),
        total=Sum('bon_total'),
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
    })