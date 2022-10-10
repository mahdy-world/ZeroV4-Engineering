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
from django.template.loader import render_to_string
from Invoices.models import *
from Factories.models import *
from django.db.models import F

# Create your views here.

class ProductList(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = Product
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
    

class ProductTrachList(LoginRequiredMixin, ListView):
    login_url = '/auth/login'
    model = Product
    paginate_by = 12
    
    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=True).order_by('-id')
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'trach'
        context['count'] = self.model.objects.filter(deleted=True).count()
        return context


class ProductCreate(LoginRequiredMixin, CreateView):
    login_url = '/auth/login/'
    model = Product
    form_class = ProductForm
    template_name = 'forms/product_form.html'
    success_url = reverse_lazy('Products:ProductList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'اضافة منتج جديد'
        context['message'] = 'add'
        context['action_url'] = reverse_lazy('Products:ProductCreate')
        return context
    
    def get_success_url(self):
        messages.success(self.request, "تم اضافة منتج جديد", extra_tags="success")

        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url


class ProductUpdate(LoginRequiredMixin ,UpdateView):
    login_url = '/auth/login/'
    model = Product
    form_class = ProductFormUpdate
    template_name = 'forms/product_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل المنتج: ' + str(self.object)
        context['message'] = 'update'
        context['action_url'] = reverse_lazy('Products:ProductUpdate', kwargs={'pk': self.object.id})
        return context
    
    def get_success_url(self):
        messages.success(self.request,  "تم تعديل المنتج " + str(self.object) + " بنجاح ", extra_tags="success")
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url            


class AddProductQuantity(LoginRequiredMixin ,UpdateView):
    login_url = '/auth/login/'
    model = Product
    form_class = ProductQuantityForm
    template_name = 'forms/form_template.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'اضافة كمية للمنتج: ' + str(self.object)
        context['message'] = 'add'
        context['action_url'] = reverse_lazy('Products:AddProductQuantity', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        myform = Product.objects.get(id=self.kwargs['pk'])
        myform.quantity += int(form.cleaned_data.get("add_quant"))
        myform.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        messages.success(self.request,  "تم اضافة كمية للمنتج " + str(self.object) + " بنجاح ", extra_tags="success")
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url


class MinusProductQuantity(LoginRequiredMixin ,UpdateView):
    login_url = '/auth/login/'
    model = Product
    form_class = ProductQuantityMinusForm
    template_name = 'forms/form_template.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'خصم كمية من المنتج: ' + str(self.object)
        context['message'] = 'add'
        context['action_url'] = reverse_lazy('Products:MinusProductQuantity', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        myform = Product.objects.get(id=self.kwargs['pk'])
        if myform.quantity >= int(form.cleaned_data.get("add_quant")):
            myform.quantity -= int(form.cleaned_data.get("add_quant"))
            myform.save()
            messages.success(self.request, "تم خصم كمية من المنتج " + str(self.object) + " بنجاح ",
                             extra_tags="success")
        else:
            messages.error(self.request, "خطأ! لم يتم خصم الكمية من المنتج " + str(self.object) + " تأكد من توفر الكمية ",
                             extra_tags="danger")

        return redirect(self.get_success_url())

    def get_success_url(self):
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url


class ProductDelete(LoginRequiredMixin ,UpdateView):
    login_url = '/auth/login/'
    model = Product
    form_class = ProductDeleteForm
    template_name = 'forms/product_form.html'
    

    def get_success_url(self):
        return reverse('Products:ProductList')
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'نقل المنتج الي سلة المهملات: ' + str(self.object)
        context['message'] = 'delete'
        context['action_url'] = reverse_lazy('Products:ProductDelete', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        messages.success(self.request, " تم نقل المنتج " + str(self.object) + ' الي سلة المهملات بنجاح ' , extra_tags="success")
        myform = Product.objects.get(id=self.kwargs['pk'])
        myform.deleted = 1
        myform.save()
        return redirect(self.get_success_url())                


class ProductRestore(LoginRequiredMixin ,UpdateView):
    login_url = '/auth/login/'
    model = Product
    form_class = ProductDeleteForm
    template_name = 'forms/product_form.html'
    

    def get_success_url(self):
        return reverse('Products:ProductList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'استرجاع منتج: ' + str(self.object)
        context['message'] = 'restore'
        context['action_url'] = reverse_lazy('Products:ProductRestore', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        messages.success(self.request, " تم استرجاع المنتج " + str(self.object) + ' الي القائمة بنجاح ' , extra_tags="success")
        myform = Product.objects.get(id=self.kwargs['pk'])
        myform.deleted = 0
        myform.save()
        return redirect(self.get_success_url())
    

class ProductSuperDelete(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = Product
    form_class = ProductDeleteForm
    template_name = 'forms/product_form.html'

    def get_success_url(self):
        return reverse('Products:ProductTrachList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'حذف المنتج: ' + str(self.object)
        context['message'] = 'super_delete'
        context['action_url'] = reverse_lazy('Products:ProductSuperDelete', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        messages.success(self.request, " تم حذف المنتج " + str(self.object) + " نهائيا بنجاح ", extra_tags="success")
        my_form = Product.objects.get(id=self.kwargs['pk'])
        my_form.delete()
        return redirect(self.get_success_url())


###################################################################


class SellerList(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = ProductSellers
    paginate_by = 12

    def get_queryset(self):
        qureyset = self.model.objects.filter(deleted=False).order_by('-id')
        return qureyset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'list'
        context['title'] = 'قائمة التجار'
        context['page'] = 'active'
        context['count'] = self.model.objects.filter(deleted=False).count()
        return context


class SellerTrashList(LoginRequiredMixin, ListView):
    login_url = '/auth/login'
    model = ProductSellers
    paginate_by = 12

    def get_queryset(self):
        queyset = self.model.objects.filter(deleted=True).order_by('-id')
        return queyset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'trach'
        context['count'] = self.model.objects.filter(deleted=True).count()
        return context


class SellerCreate(LoginRequiredMixin, CreateView):
    login_url = '/auth/login/'
    model = ProductSellers
    form_class = ProductSellerForm
    template_name = 'forms/form_template.html'
    success_url = reverse_lazy('Products:SellerList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'اضافة تاجر جديد'
        context['message'] = 'add'
        context['action_url'] = reverse_lazy('Products:SellerCreate')
        return context

    def get_success_url(self):
        messages.success(self.request, "تم اضافة تاجر جديد", extra_tags="success")

        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url


class SellerUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = ProductSellers
    form_class = ProductSellerFormUpdate
    template_name = 'forms/form_template.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل التاجر: ' + str(self.object)
        context['message'] = 'update'
        context['action_url'] = reverse_lazy('Products:SellerUpdate', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self):
        messages.success(self.request, "تم تعديل التاجر " + str(self.object) + " بنجاح ", extra_tags="success")
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url


class PaidSellerValue(LoginRequiredMixin, CreateView):
    login_url = '/auth/login/'
    model = SellerPayments
    form_class = ProductSellerPaymentForm
    template_name = 'forms/form_template.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'استلام مبلغ من التاجر: ' + str(ProductSellers.objects.get(id=self.kwargs['pk']).name)
        context['message'] = 'add'
        context['action_url'] = reverse_lazy('Products:PaidSellerValue', kwargs={'pk': self.kwargs['pk']})
        return context

    def form_valid(self, form):
        seller = ProductSellers.objects.get(id=self.kwargs['pk'])
        myform = SellerPayments()
        myform.seller = seller
        myform.paid_value = form.cleaned_data.get("paid_value")
        myform.paid_reason = form.cleaned_data.get("paid_reason")
        myform.paid_type = 1
        myform.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        messages.success(self.request, "تم استلام مبلغ من التاجر " + str(ProductSellers.objects.get(id=self.kwargs['pk']).name) + " بنجاح ", extra_tags="success")
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url


class PaidSellerValue2(LoginRequiredMixin, CreateView):
    login_url = '/auth/login/'
    model = SellerPayments
    form_class = ProductSellerPaymentForm
    template_name = 'forms/form_template.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تسليم مبلغ الي التاجر: ' + str(ProductSellers.objects.get(id=self.kwargs['pk']).name)
        context['message'] = 'add'
        context['action_url'] = reverse_lazy('Products:PaidSellerValue2', kwargs={'pk': self.kwargs['pk']})
        return context

    def form_valid(self, form):
        seller = ProductSellers.objects.get(id=self.kwargs['pk'])
        myform = SellerPayments()
        myform.seller = seller
        myform.paid_value = form.cleaned_data.get("paid_value")
        myform.paid_reason = form.cleaned_data.get("paid_reason")
        myform.paid_type = 2
        myform.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        messages.success(self.request, "تم تسليم مبلغ الي التاجر " + str(ProductSellers.objects.get(id=self.kwargs['pk']).name) + " بنجاح ", extra_tags="success")
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url


class SellerDelete(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = ProductSellers
    form_class = ProductSellerDeleteForm
    template_name = 'forms/form_template.html'

    def get_success_url(self):
        return reverse('Products:SellerList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'نقل التاجر الي سلة المهملات: ' + str(self.object)
        context['message'] = 'delete'
        context['action_url'] = reverse_lazy('Products:SellerDelete', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        messages.success(self.request, " تم نقل التاجر " + str(self.object) + ' الي سلة المهملات بنجاح ', extra_tags="success")
        myform = ProductSellers.objects.get(id=self.kwargs['pk'])
        myform.deleted = 1
        myform.save()
        return redirect(self.get_success_url())


class SellerRestore(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = ProductSellers
    form_class = ProductSellerDeleteForm
    template_name = 'forms/form_template.html'

    def get_success_url(self):
        return reverse('Products:SellerList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'استرجاع تاجر: ' + str(self.object)
        context['message'] = 'restore'
        context['action_url'] = reverse_lazy('Products:SellerRestore', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        messages.success(self.request, " تم استرجاع التاجر " + str(self.object) + ' الي القائمة بنجاح ', extra_tags="success")
        myform = ProductSellers.objects.get(id=self.kwargs['pk'])
        myform.deleted = 0
        myform.save()
        return redirect(self.get_success_url())


class SellerSuperDelete(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = ProductSellers
    form_class = ProductSellerDeleteForm
    template_name = 'forms/form_template.html'

    def get_success_url(self):
        return reverse('Products:SellerTrashList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'حذف التاجر: ' + str(self.object)
        context['message'] = 'super_delete'
        context['action_url'] = reverse_lazy('Products:SellerSuperDelete', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        messages.success(self.request, " تم حذف التاجر " + str(self.object) + " نهائيا بنجاح ", extra_tags="success")
        my_form = ProductSellers.objects.get(id=self.kwargs['pk'])
        my_form.delete()
        return redirect(self.get_success_url())


class SellerDetails(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = SellerPayments
    template_name = 'Products/productsellers_detail.html'
    # paginate_by = 5

    def get_queryset(self):
        queryset = SellerPayments.objects.filter(seller=self.kwargs['pk'], paid_value__gt=0).order_by('-date')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'عمليات استلام/تسليم مبالغ من/الي التاجر: ' + str(ProductSellers.objects.get(id=self.kwargs['pk']).name)
        context['type'] = 'list'
        context['seller'] = ProductSellers.objects.get(id=int(self.kwargs['pk']))
        context['from'] = SellerPayments.objects.filter(seller=int(self.kwargs['pk']), paid_value__gt=0, paid_type=1).aggregate(sum=Sum('paid_value'))
        context['to'] = SellerPayments.objects.filter(seller=int(self.kwargs['pk']), paid_value__gt=0, paid_type=2).aggregate(sum=Sum('paid_value'))
        context['count'] = SellerPayments.objects.filter(seller=self.kwargs['pk'], paid_value__gt=0).order_by('date').count()
        return context


class SellerInvoices(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = Invoice
    template_name = 'Products/productsellers_invoice.html'
    # paginate_by = 5

    # def get_queryset(self):
    #     queryset = Invoice.objects.filter(seller=self.kwargs['pk']).order_by('-date')
    #     return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'فواتير التاجر: ' + str(ProductSellers.objects.get(id=self.kwargs['pk']).name)
        context['type'] = 'list'

        context['invoices'] = Invoice.objects.filter(seller=self.kwargs['pk'], invoice_type=1).order_by('-date')
        context['invoices_sum'] = Invoice.objects.filter(seller=self.kwargs['pk'], invoice_type=1).order_by('-date').aggregate(sum=Sum(F('total') - F('discount'))).get('sum')
        context['invoices_r_sum'] = Invoice.objects.filter(seller=self.kwargs['pk'], invoice_type=1).order_by('-date').aggregate(sum=Sum('return_value')).get('sum')
        context['r_invoices'] = Invoice.objects.filter(seller=self.kwargs['pk'], invoice_type=2).order_by('-date')
        context['r_invoices_sum'] = Invoice.objects.filter(seller=self.kwargs['pk'], invoice_type=2).order_by('-date').aggregate(sum=Sum(F('total') - F('discount'))).get('sum')

        if context['invoices_sum']:
            context['invoices_sum'] = context['invoices_sum']
        else:
            context['invoices_sum'] = 0.0

        if context['invoices_r_sum']:
            context['invoices_r_sum'] = context['invoices_r_sum']
        else:
            context['invoices_r_sum'] = 0.0

        if context['r_invoices_sum']:
            context['r_invoices_sum'] = context['r_invoices_sum']
        else:
            context['r_invoices_sum'] = 0.0

        context['seller'] = ProductSellers.objects.get(id=int(self.kwargs['pk']))
        return context


def PrintSellerInvoicesDetails(request, pk):
    seller = ProductSellers.objects.get(id=pk)
    system_info = SystemInformation.objects.all()
    if system_info.count() > 0:
        system_info = system_info.last()
    else:
        system_info = None

    invoices = Invoice.objects.filter(seller=seller, invoice_type=1).order_by('-date')
    invoices_sum = invoices.aggregate(sum=Sum(F('total') - F('discount'))).get('sum')
    invoices_r_sum = invoices.aggregate(sum=Sum('return_value')).get('sum')
    r_invoices = Invoice.objects.filter(seller=seller, invoice_type=2).order_by('-date')
    r_invoices_sum = r_invoices.aggregate(sum=Sum(F('total') - F('discount'))).get('sum')

    if invoices_sum:
        invoices_sum = invoices_sum
    else:
        invoices_sum = 0.0

    if invoices_r_sum:
        invoices_r_sum = invoices_r_sum
    else:
        invoices_r_sum = 0.0

    if r_invoices_sum:
        r_invoices_sum = r_invoices_sum
    else:
        r_invoices_sum = 0.0

    seller_payments_from = SellerPayments.objects.filter(seller=seller, paid_type=1, paid_value__gt=0)
    seller_payments_to = SellerPayments.objects.filter(seller=seller, paid_type=2, paid_value__gt=0)
    if seller:
        initial_debit = seller.initial_balance_debit
    else:
        initial_debit = 0

    if seller_payments_from:
        payments_from = seller_payments_from.aggregate(sum=Sum('paid_value')).get('sum')
    else:
        payments_from = 0

    if seller_payments_to:
        payments_to = seller_payments_to.aggregate(sum=Sum('paid_value')).get('sum')
    else:
        payments_to = 0

    payment_s = payments_from - payments_to
    if seller.initial_balance_type == 1:
        payment_sum = (payments_from - payments_to) + initial_debit
    else:
        payment_sum = (payments_from - payments_to) - initial_debit

    context = {
        'system_info': system_info,
        'date': datetime.now(),
        'user': request.user.username,
        'seller': seller,
        'invoices': invoices,
        'invoices_sum': invoices_sum,
        'r_invoices': r_invoices,
        'r_invoices_sum': r_invoices_sum,
        'payment_sum': payment_sum,
        'invoices_r_sum': invoices_r_sum,
        'seller_payments_from': seller_payments_from,
        'seller_payments_to': seller_payments_to,
        'payments_from': payments_from,
        'payments_to': payments_to,
        'payment_s': payment_s,
    }
    html_string = render_to_string('Products/print_seller_invoices_details.html', context)
    html = weasyprint.HTML(string=html_string, base_url=request.build_absolute_uri())
    pdf = html.write_pdf(stylesheets=[weasyprint.CSS('static/assets/css/invoice_pdf.css')], presentational_hints=True)
    response = HttpResponse(pdf, content_type='application/pdf')
    return response


class ProductDetails(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = Invoice
    template_name = 'Products/product_detail.html'

    def get_context_data(self, **kwargs):
        product = Product.objects.get(id=int(self.kwargs['pk']))
        context = super().get_context_data(**kwargs)
        context['title'] = 'إنتاج ومبيعات الموديل: ' + str(product.name)
        context['type'] = 'list'
        context['factory_in'] = FactoryInSide.objects.filter(product=product).order_by('-date', '-id')
        context['factory_in_sum'] = FactoryInSide.objects.filter(product=product).order_by('-date', '-id').aggregate(sum=Sum('product_count')).get('sum')

        context['invoices'] = InvoiceItem.objects.filter(item=product, invoice__invoice_type__in=[1, 3], invoice__saved=True).order_by('-date', '-id')
        context['invoices_sum'] = InvoiceItem.objects.filter(item=product, invoice__invoice_type__in=[1, 3], invoice__saved=True).order_by('-date', '-id').aggregate(sum=Sum(F('quantity') * F('unit'))).get('sum')
        context['r_invoices'] = InvoiceItem.objects.filter(item=product, invoice__invoice_type=2, invoice__saved=True).order_by('-date', '-id')
        context['r_invoices_sum'] = InvoiceItem.objects.filter(item=product, invoice__invoice_type=2, invoice__saved=True).order_by('-date', '-id').aggregate(sum=Sum(F('quantity') * F('unit'))).get('sum')

        if context['factory_in_sum']:
            context['factory_in_sum'] = context['factory_in_sum']
        else:
            context['factory_in_sum'] = 0

        if context['invoices_sum']:
            context['invoices_sum'] = context['invoices_sum']
        else:
            context['invoices_sum'] = 0

        if context['r_invoices_sum']:
            context['r_invoices_sum'] = context['r_invoices_sum']
        else:
            context['r_invoices_sum'] = 0

        context['total'] = context['factory_in_sum'] - (context['invoices_sum'] - context['r_invoices_sum'])

        context['product'] = product
        return context