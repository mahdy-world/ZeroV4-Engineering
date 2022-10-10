import datetime
import json

from django.db.models.aggregates import Sum
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import *

from Core.models import SystemInformation
from .forms import *

from django.contrib import messages
import weasyprint
from django.template.loader import render_to_string
from datetime import datetime


class FactoryList(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = Factory
    paginate_by = 12
    template_name = 'Factory/factory_list.html'
    
    def get_queryset(self):
        qureyset = self.model.objects.filter(deleted=False).order_by('-id')
        return qureyset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'list'
        context['title'] = 'قائمة المصانع'
        context['icons'] = '<i class="fas fa-shapes"></i>'
        context['page'] = 'active'
        context['count'] = self.model.objects.filter(deleted=False).count()
        return context



class FactoryTrachList(LoginRequiredMixin, ListView):
    login_url = '/auth/login'
    model = Factory
    paginate_by = 12
    template_name = 'Factory/factory_list.html'
    
    def get_queryset(self):
        queyset = self.model.objects.filter(deleted=True).order_by('-id')
        return queyset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'trach'
        context['count'] = self.model.objects.filter(deleted=True).count()
        return context



class FactoryCreate(LoginRequiredMixin, CreateView):
    login_url = '/auth/login/'
    model = Factory
    form_class = FactoryForm
    template_name = 'forms/factory_form.html'
    success_url = reverse_lazy('Factories:FactoryList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'اضافة مصنع جديد'
        context['message'] = 'add'
        context['action_url'] = reverse_lazy('Factories:FactoryCreate')
        return context
    
    def get_success_url(self):
        messages.success(self.request, "تم اضافة مصنع جديد", extra_tags="success")

        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url
        



class FactoryUpdate(LoginRequiredMixin ,UpdateView):
    login_url = '/auth/login/'
    model = Factory
    form_class = FactoryForm
    template_name = 'forms/factory_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل مصنع: ' + str(self.object)
        context['message'] = 'update'
        context['action_url'] = reverse_lazy('Factories:FactoryUpdate', kwargs={'pk': self.object.id})
        return context
    
    def get_success_url(self):
        messages.success(self.request,  "تم تعديل المصنع " + str(self.object) + " بنجاح ", extra_tags="success")
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url
                


class FactoryDelete(LoginRequiredMixin ,UpdateView):
    login_url = '/auth/login/'
    model = Factory
    form_class = FactoryDeleteForm
    template_name = 'forms/factory_form.html'
    

    def get_success_url(self):
        return reverse('Factories:FactoryList')
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'نقل المصنع الي سلة المهملات: ' + str(self.object)
        context['message'] = 'delete'
        context['action_url'] = reverse_lazy('Factories:FactoryDelete', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        messages.success(self.request, " تم نقل المصنع " + str(self.object) + ' الي سلة المهملات بنجاح ' , extra_tags="success")
        myform = Factory.objects.get(id=self.kwargs['pk'])
        myform.deleted = 1
        myform.save()
        return redirect(self.get_success_url())        



class FactoryRestore(LoginRequiredMixin ,UpdateView):
    login_url = '/auth/login/'
    model = Factory
    form_class = FactoryDeleteForm
    template_name = 'forms/factory_form.html'
    

    def get_success_url(self):
        return reverse('Factories:FactoryList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'استرجاع مصنع: ' + str(self.object)
        context['message'] = 'restore'
        context['action_url'] = reverse_lazy('Factories:FactoryRestore', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        messages.success(self.request, " تم المصنع " + str(self.object) + ' الي القائمة بنجاح ' , extra_tags="success")
        myform = Factory.objects.get(id=self.kwargs['pk'])
        myform.deleted = 0
        myform.save()
        return redirect(self.get_success_url())
    

class FactorySuperDelete(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = Factory
    form_class = FactoryDeleteForm
    template_name = 'forms/form_template.html'

    def get_success_url(self):
        return reverse('Factories:FactoryTrachList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'حذف المصنع : ' + str(self.object)
        context['message'] = 'super_delete'
        context['action_url'] = reverse_lazy('Factories:FactorySuperDelete', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        messages.success(self.request, " تم حذف المصنع " + str(self.object) + " نهائيا بنجاح ", extra_tags="success")
        my_form = Factory.objects.get(id=self.kwargs['pk'])
        my_form.delete()
        return redirect(self.get_success_url())    


class FactoryPayment(LoginRequiredMixin, DetailView):
    login_url = '/auth/login/'
    model = Factory
    template_name = 'Factory/factory_payment.html'
    
    def get_context_data(self, **kwargs):
        queryset = Payment.objects.filter(factory=self.object)
        payment_sum = queryset.aggregate(price=Sum('price')).get('price')
        total_account =FactoryInSide.objects.filter(factory=self.object).aggregate(total=Sum('total_account')).get('total')
        total = ''
        if total_account and payment_sum != None:
            total = total_account - payment_sum
        
        
        context = super().get_context_data(**kwargs)
        context['payment'] = queryset.order_by('-date')
        context['payment_sum'] = payment_sum
        context['total_account'] = total_account
        context['total'] = total
        context['title'] = 'مسحوبات مصنع: ' + str(self.object)
        context['form'] = FactoryPaymentForm(self.request.POST or None)
        context['type'] = 'list'
        context['factory'] = self.object
        return context
    
    
class FactoryPayment_div(LoginRequiredMixin, DetailView):
    login_url = '/auth/login/'
    model = Factory
    template_name = 'Factory/payment_div.html'
    
    def get_context_data(self, **kwargs):
        queryset = Payment.objects.filter(factory=self.object).order_by('-date')
        payment_sum = queryset.aggregate(price=Sum('price')).get('price')
        total_account =FactoryInSide.objects.filter(factory=self.object).aggregate(total=Sum('total_account')).get('total')
        total = ''
        if total_account and payment_sum != None:
            total = total_account - payment_sum
        
        
        context = super().get_context_data(**kwargs)
        context['payment'] = queryset.order_by('-date')
        context['payment_sum'] = payment_sum
        context['total_account'] = total_account
        context['total'] = total
        context['title'] = 'مسحوبات مصنع: ' + str(self.object)
        context['form'] = FactoryPaymentForm(self.request.POST or None)
        context['type'] = 'list'
        context['factory'] = self.object
        return context


class FactoryPaymentUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = Payment
    form_class = FactoryPaymentForm
    template_name = 'forms/form_template.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل  مسحوبات يوم : ' + str(self.object)
        context['message'] = 'update'
        context['action_url'] = reverse_lazy('Factories:FactoryPaymentUpdate', kwargs={'pk': self.object.id})
        return context 
    
    def get_success_url(self):
        messages.success(self.request, " تم تعديل المسحوبات " + str(self.object) + " بنجاح ", extra_tags="success")
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url

         

def FactoryPaymentCreate(request):
    if request.is_ajax():
        factory_id = request.POST.get('id')
        factory = Factory.objects.get(id=factory_id)
        
        date = request.POST.get('date')
        recipient = request.POST.get('recipient')
        price = request.POST.get('price')
        
        if factory_id and date and recipient and price:
            obj = Payment()
            obj.factory = factory
            obj.date = date
            obj.admin = request.user
            obj.recipient = recipient
            obj.price = price
            obj.save()
            
            if obj:
                response = {
                    'msg' : 1
                }
        else:
            response = {
                'msg' : 0
            }
        return JsonResponse(response)

    
def FactoryPaymentDelete(request):
    if request.is_ajax():
        payment_id = request.POST.get('payment_id')
        obj =  Payment.objects.get(id=payment_id)
        obj.delete()
        
        if obj:
            response = {
                'msg' : 'Send Successfully'
            }

        return JsonResponse(response)


class FactoryOutside(LoginRequiredMixin, DetailView):
    login_url = '/auth/login/'
    model = Factory
    template_name = 'Factory/factory_outside.html'
    
    def get_context_data(self, **kwargs):
        queryset = FactoryOutSide.objects.filter(factory=self.object)
        context = super().get_context_data(**kwargs)
        context['outSide'] = queryset.order_by('-date')
        context['title'] = 'الخارج من المصنع: ' + str(self.object)
        sum_weight = queryset.aggregate(weight=Sum('weight')).get('weight')
        if sum_weight:
            context['sum_weight'] = "{:.1f}".format(sum_weight)
        else:
            context['sum_weight'] = 0
        sum_weight_after = queryset.aggregate(after=Sum('weight_after_loss')).get('after')
        if sum_weight_after:
            context['sum_weight_after'] = "{:.1f}".format(sum_weight_after)
        else:
            context['sum_weight_after'] = 0
        form = FactoryOutSideForm(self.request.POST or None)
        form.fields['percent_loss'].initial = 0
        context['form'] = form
        context['type'] = 'list'
        context['factory'] = self.object
        return context
    

class FactoryOutSide_div(LoginRequiredMixin, DetailView):
    login_url = '/auth/login/'
    model = Factory
    template_name = 'Factory/outside_div.html'
    
    def get_context_data(self, **kwargs):
        queryset = FactoryOutSide.objects.filter(factory=self.object)
        context = super().get_context_data(**kwargs)
        context['outSide'] = queryset.order_by('-date')
        sum_weight = queryset.aggregate(weight=Sum('weight')).get('weight')
        context['sum_weight'] = "{:.1f}".format(sum_weight)
        sum_weight_after = queryset.aggregate(after=Sum('weight_after_loss')).get('after')
        context['sum_weight_after'] = "{:.1f}".format(sum_weight_after)
        form = FactoryOutSideForm(self.request.POST or None)
        form.fields['percent_loss'].initial = 0
        context['form'] = form
        context['factory'] = self.object
        return context    


def FactoryOutSideCreate(request):
    if request.is_ajax():
        factory_id = request.POST.get('id')
        factory = Factory.objects.get(id=factory_id)
        
        date = request.POST.get('date')
        weight = request.POST.get('weight')
        color = request.POST.get('color')
        wool_type = request.POST.get('wool_type')
        percent_loss = request.POST.get('percent_loss')
        weight_after_loss = request.POST.get('weight_after_loss')

        if factory_id and date and weight and percent_loss and weight_after_loss:
            obj = FactoryOutSide()
            obj.factory = factory
            obj.date = date
            obj.admin = request.user
            obj.weight = weight
            obj.color = color
            if wool_type:
                obj.wool_type = wool_type
            else:
                obj.wool_type = None
            obj.percent_loss = percent_loss
            obj.weight_after_loss = weight_after_loss
            obj.save()
            
            if obj:
                response = {
                    'msg' : 1
                }
        else:
            response = {
                'msg' : 0
            }
        return JsonResponse(response)
        
          
class FactoryOutSideUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = FactoryOutSide
    form_class =  FactoryOutSideForm
    template_name = 'forms/form_template.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل الخارج يوم : ' + str(self.object)
        context['message'] = 'update'
        context['action_url'] = reverse_lazy('Factories:FactoryOutSideUpdate', kwargs={'pk': self.object.id})
        return context 
    
    def get_success_url(self):
        messages.success(self.request, " تم تعديل الخارج " + str(self.object) + " بنجاح ", extra_tags="success")
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url
          
    
def FactoryOutsideDelete(request):
    if request.is_ajax():
        outside_id = request.POST.get('outside_id')
        obj =  FactoryOutSide.objects.get(id=outside_id)
        obj.delete()
        
        if obj:
            response = {
                'msg' : 'Send Successfully'
            }

        return JsonResponse(response)
 

class FactoryInside(LoginRequiredMixin, DetailView):
    login_url = '/auth/login/'
    model = Factory
    template_name = 'Factory/factory_inside.html'
    
    def get_context_data(self, **kwargs):
        queryset = FactoryInSide.objects.filter(factory=self.object)
        outSide = FactoryOutSide.objects.filter(factory=self.object)
        context = super().get_context_data(**kwargs)
        context['inSide'] = queryset.order_by('-date')
        context['title'] = 'الداخل لمصنع: ' + str(self.object)
        form = FactoryInSideForm(self.request.POST or None)
        form.fields['hour_price'].initial = self.object.hour_price
        form.fields['product'].queryset = Product.objects.filter(deleted=0)
        context['form'] = form
        sum_outside = outSide.aggregate(out=Sum('weight_after_loss')).get('out')
        context['sum_outside'] = sum_outside
        sum_weight = queryset.aggregate(weight=Sum('weight')).get('weight')
        context['sum_weight'] = sum_weight
        sum_weight_after = queryset.aggregate(after=Sum('total_account')).get('after')
        context['sum_weight_after'] = sum_weight_after
        context['type'] = 'list'
        context['factory'] = self.object
        return context


class FactoryInSideUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = FactoryInSide
    form_class =  FactoryInSideForm
    template_name = 'forms/form_template.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل الداخل  : ' + str(self.object)
        context['message'] = 'update'
        context['action_url'] = reverse_lazy('Factories:FactoryInSideUpdate', kwargs={'pk': self.object.id})
        return context 
    
    def get_success_url(self):
        messages.success(self.request, " تم تعديل الداخل " + str(self.object) + " بنجاح ", extra_tags="success")
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url
    

class FactoryInSide_div(LoginRequiredMixin, DetailView):
    login_url = '/auth/login/'
    model = Factory
    template_name = 'Factory/inside_div.html'
    
    def get_context_data(self, **kwargs):
        queryset = FactoryInSide.objects.filter(factory=self.object)
        outSide = FactoryOutSide.objects.filter(factory=self.object)
        context = super().get_context_data(**kwargs)
        context['inSide'] = queryset.order_by('-date')
        sum_outside = outSide.aggregate(out=Sum('weight_after_loss')).get('out')
        context['sum_outside'] = "{:.1f}".format(sum_outside)
        sum_weight = queryset.aggregate(weight=Sum('weight')).get('weight')
        context['sum_weight'] = "{:.1f}".format(sum_weight)
        sum_weight_after = queryset.aggregate(after=Sum('total_account')).get('after')
        context['sum_weight_after'] = "{:.1f}".format(sum_weight_after)
        form = FactoryInSideForm(self.request.POST or None)
        form.fields['hour_price'].initial = self.object.hour_price
        context['form'] = form
        context['factory'] = self.object
        return context    

      
def FactoryInSideCreate(request):
    if request.is_ajax():
        factory_id = request.POST.get('id')
        factory = Factory.objects.get(id=factory_id) 
        print(factory)
        date = request.POST.get('date')
        weight = request.POST.get('weight')
        color = request.POST.get('color')
        wool_type = request.POST.get('wool_type')
        product = request.POST.get('product')
        product_weight = request.POST.get('product_weight')
        product_time = request.POST.get('product_time')
        product_count = request.POST.get('product_count')
        hour_count = request.POST.get('hour_count')
        hour_price = request.POST.get('hour_price')
        total_account = request.POST.get('total_account')
        
        if factory_id and date and weight and product and product_weight and product_count and product_time and hour_count and hour_price and total_account:
    
            obj = FactoryInSide()
            obj.factory = factory
            obj.date = date
            obj.weight = weight
            obj.color = color
            if wool_type:
                obj.wool_type = wool_type
            else:
                obj.wool_type = None
            obj.product = Product.objects.get(id=product)
            obj.product_weight = product_weight
            obj.product_time = product_time
            obj.product_count = product_count
            obj.hour_count = hour_count
            obj.hour_price = hour_price
            obj.total_account = total_account
            obj.admin = request.user
            obj.save()
        
            if obj:
                response = {
                'msg' : 1
                }
            else:
                response = {
                    'msg' : 0
                }

            prod = obj.product
            if prod.quantity:
                prod.quantity += int(obj.product_count)
            else:
                prod.quantity = int(obj.product_count)
            prod.save(update_fields=['quantity'])

        return JsonResponse(response)
        
    
def FactoryInsideDelete(request):
    if request.is_ajax():
        inside_id = request.POST.get('inside_id')
        obj =  FactoryInSide.objects.get(id=inside_id)
        obj.delete()
        
        if obj:
            response = {
                'msg' : 'Send Successfully'
            }

        return JsonResponse(response)    
        


class FactoryPaymentReport(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = Payment
    form = FactoryPaymentReportForm()
    template_name = 'Factory_Reports/factory_payment_report.html'
    
   
    def queryset(self):
        if not self.request.GET.get('submit'):
            queryset = None
        else:
            queryset = Payment.objects.filter(factory = self.kwargs['pk']).order_by('-id')
            if self.request.GET.get('from_date'):
                queryset = queryset.filter(date__gte = self.request.GET.get('from_date'))
            if self.request.GET.get('to_date'):
                queryset = queryset.filter(date__lte = self.request.GET.get('to_date'))
                                  
        return queryset 
    
    def get_sum_price(self):
        queryset = self.queryset()
        if queryset != None:
            sum_price =  queryset.aggregate(price=Sum('price')).get('price')
        else:
            sum_price = 0
        total = {
            'sum_price' :sum_price
        }
        return total
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        context['summary'] = self.get_sum_price()
        context['name'] = Factory.objects.get(id=self.kwargs['pk'])
        return context
    
    
class FactoryOutSideReport(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = FactoryOutSide
    form = FactoryPaymentReportForm()
    template_name = 'Factory_Reports/factory_outside_report.html'
    
   
    def queryset(self):
        if not self.request.GET.get('submit'):
            queryset = None
        else:
            queryset = FactoryOutSide.objects.filter(factory = self.kwargs['pk']).order_by('-id')
            if self.request.GET.get('from_date'):
                queryset = queryset.filter(date__gte = self.request.GET.get('from_date'))
            if self.request.GET.get('to_date'):
                queryset = queryset.filter(date__lte = self.request.GET.get('to_date'))
                                  
        return queryset 
    
    def get_sum_outside(self):
        queryset = self.queryset()
        if queryset != None:
            sum_weight =  queryset.aggregate(out=Sum('weight_after_loss')).get('out')
        else:
            sum_weight = 0
            
        sum_weight = "{:.1f}".format(sum_weight)
        total = {
            'sum_weight' :sum_weight
        }
        return total
    
    
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        context['summary'] = self.get_sum_outside()
        context['name'] = Factory.objects.get(id=self.kwargs['pk'])
        return context
    
    
class FactoryInSideReport(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = FactoryInSide
    form = FactoryPaymentReportForm()
    template_name = 'Factory_Reports/factory_inside_report.html'
    
   
    def queryset(self):
        if not self.request.GET.get('submit'):
            queryset = None
        else:
            queryset = FactoryInSide.objects.filter(factory = self.kwargs['pk']).order_by('-id')
            if self.request.GET.get('from_date'):
                queryset = queryset.filter(date__gte = self.request.GET.get('from_date'))
            if self.request.GET.get('to_date'):
                queryset = queryset.filter(date__lte = self.request.GET.get('to_date'))
                                  
        return queryset 
    
    def get_sum_inside(self):
        queryset = self.queryset()
        if queryset != None:
            sum_weight =  queryset.aggregate(out=Sum('total_account')).get('out')
        else:
            sum_weight = 0
            
        sum_weight = "{:.1f}".format(sum_weight)
        total = {
            'sum_weight' :sum_weight
        }
        return total
    
    
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        context['summary'] = self.get_sum_inside()
        context['name'] = Factory.objects.get(id=self.kwargs['pk'])
        return context
    



def PrintPayment(request,pk):
    factory = Factory.objects.get(id=pk)
    system_info = SystemInformation.objects.all()
    if system_info.count() > 0:
        system_info = system_info.last()
    else:
        system_info = None
            
    queryset = Payment.objects.filter(factory=pk).order_by('-date')
    if request.GET.get('from_date'):
        queryset = queryset.filter(date__gte = request.GET.get('from_date'))
    if request.GET.get('to_date'):
        queryset = queryset.filter(date__lte = request.GET.get('to_date'))
    
   
    context = {
        'queryset':queryset,
        'count_price':  queryset.aggregate(price=Sum('price')).get('price'),
        'system_info':system_info,
        'date': datetime.now(),
        'user': request.user.username,
        'from_date': request.GET.get('from_date'),
        'to_date': request.GET.get('to_date'),
        'factory':factory,
    }
    html_string = render_to_string('Factory_Reports/print_payment.html', context)
    html = weasyprint.HTML(string=html_string, base_url=request.build_absolute_uri())
    pdf = html.write_pdf(stylesheets=[weasyprint.CSS('static/assets/css/invoice_pdf.css')], presentational_hints=True)
    response = HttpResponse(pdf, content_type='application/pdf')
    return response



def PrintOutside(request,pk):
    factory = Factory.objects.get(id=pk)
    system_info = SystemInformation.objects.all()
    if system_info.count() > 0:
        system_info = system_info.last()
    else:
        system_info = None
            
    queryset = FactoryOutSide.objects.filter(factory=pk).order_by('-date')
    if request.GET.get('from_date'):
        queryset = queryset.filter(date__gte = request.GET.get('from_date'))
    if request.GET.get('to_date'):
        queryset = queryset.filter(date__lte = request.GET.get('to_date'))
    
    sum_weight = queryset.aggregate(out=Sum('weight_after_loss')).get('out')
    # sum_weight = "{:.3f}".format(sum_weight)
    context = {
        'queryset':queryset,
        'sum_weight':sum_weight,
        'system_info':system_info,
        'date': datetime.now(),
        'user': request.user.username,
        'from_date': request.GET.get('from_date'),
        'to_date': request.GET.get('to_date'),
        'factory':factory,
    }
    html_string = render_to_string('Factory_Reports/print_outside.html', context)
    html = weasyprint.HTML(string=html_string, base_url=request.build_absolute_uri())
    pdf = html.write_pdf(stylesheets=[weasyprint.CSS('static/assets/css/invoice_pdf.css')], presentational_hints=True)
    response = HttpResponse(pdf, content_type='application/pdf')
    return response



def PrintInside(request,pk):
    factory = Factory.objects.get(id=pk)
    system_info = SystemInformation.objects.all()
    if system_info.count() > 0:
        system_info = system_info.last()
    else:
        system_info = None
            
    queryset = FactoryInSide.objects.filter(factory=pk).order_by('-date')
    if request.GET.get('from_date'):
        queryset = queryset.filter(date__gte = request.GET.get('from_date'))
    if request.GET.get('to_date'):
        queryset = queryset.filter(date__lte = request.GET.get('to_date'))
    
    weight = queryset.aggregate(weight=Sum('weight')).get('weight')
    sum_weight = queryset.aggregate(out=Sum('total_account')).get('out')
    # sum_weight = "{:.2f}".format(sum_weight)
    # weight = "{:.3f}".format(weight)
    context = {
        'queryset':queryset,
        'sum_weight':sum_weight,
        'weight':weight,
        'system_info':system_info,
        'date': datetime.now(),
        'user': request.user.username,
        'from_date': request.GET.get('from_date'),
        'to_date': request.GET.get('to_date'),
        'factory':factory,
    }
    html_string = render_to_string('Factory_Reports/print_inside.html', context)
    html = weasyprint.HTML(string=html_string, base_url=request.build_absolute_uri())
    pdf = html.write_pdf(stylesheets=[weasyprint.CSS('static/assets/css/invoice_pdf.css')], presentational_hints=True)
    response = HttpResponse(pdf, content_type='application/pdf')
    return response


def get_product_weight_time(request):
    e = request.GET.get('e')
    product = Product.objects.get(id=int(e))
    if product.weight:
        weight = product.weight
    else:
        weight = 0.0
    if product.time:
        time = product.time
    else:
        time = 0.0
    data = json.dumps({
        'prod_weight': weight,
        'prod_time': time,
    })
    return HttpResponse(data, content_type='application/json')


def PrintAll(request, pk):
    factory = Factory.objects.get(id=pk)
    system_info = SystemInformation.objects.all()
    if system_info.count() > 0:
        system_info = system_info.last()
    else:
        system_info = None

    inside = FactoryInSide.objects.filter(factory=pk)
    if inside:
        sum_in_weight = inside.aggregate(weight=Sum('weight')).get('weight')
        sum_in_total = inside.aggregate(total=Sum('total_account')).get('total')
    else:
        sum_in_weight = 0
        sum_in_total = 0

    outside = FactoryOutSide.objects.filter(factory=pk)
    if outside:
        sum_out_weight = outside.aggregate(out=Sum('weight_after_loss')).get('out')
    else:
        sum_out_weight = 0

    payment = Payment.objects.filter(factory=pk)
    if payment:
        sum_out_total = payment.aggregate(price=Sum('price')).get('price')
    else:
        sum_out_total = 0

    context = {
        'sum_in_weight': sum_in_weight,
        'sum_in_total': sum_in_total,
        'sum_out_weight': sum_out_weight,
        'sum_out_total': sum_out_total,
        'system_info': system_info,
        'date': datetime.now(),
        'user': request.user.username,
        'factory': factory,
    }
    html_string = render_to_string('Factory_Reports/print_factory_details.html', context)
    html = weasyprint.HTML(string=html_string, base_url=request.build_absolute_uri())
    pdf = html.write_pdf(stylesheets=[weasyprint.CSS('static/assets/css/invoice_pdf.css')], presentational_hints=True)
    response = HttpResponse(pdf, content_type='application/pdf')
    return response


############################################################


class SupplierList(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = Supplier
    paginate_by = 12
    template_name = 'Supplier/supplier_list.html'

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=False, type=int(self.kwargs['type'])).order_by('-id')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'active'
        context['type'] = self.kwargs['type']
        context['count'] = self.model.objects.filter(deleted=False, type=int(self.kwargs['type'])).count()
        return context


class SupplierTrashList(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = Supplier
    paginate_by = 12
    template_name = 'Supplier/supplier_list.html'

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=True, type=int(self.kwargs['type'])).order_by('-id')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'trash'
        context['type'] = self.kwargs['type']
        context['count'] = self.model.objects.filter(deleted=True, type=int(self.kwargs['type'])).count()
        return context


class SupplierCreate(LoginRequiredMixin, CreateView):
    login_url = '/auth/login/'
    model = Supplier
    form_class = SupplierForm
    template_name = 'forms/form_template.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.kwargs['type'] == 1:
            context['title'] = 'اضافة مورد'
        else:
            context['title'] = 'اضافة مستورد'
        context['message'] = 'create'
        context['action_url'] = reverse_lazy('Factories:SupplierCreate', kwargs={'type': self.kwargs['type']})
        return context

    def form_valid(self, form):
        form.save()
        obj = form.save(commit=False)
        myform = Supplier.objects.get(id=obj.id)
        myform.type = int(self.kwargs['type'])
        myform.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        if self.kwargs['type'] == 1:
            messages.success(self.request, "تم اضافة مورد جديد", extra_tags="success")
        else:
            messages.success(self.request, "تم اضافة مستورد جديد", extra_tags="success")

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
        if self.object.type == 1:
            context['title'] = 'تعديل بيانات مورد: ' + str(self.object)
        else:
            context['title'] = 'تعديل بيانات مستورد: ' + str(self.object)
        context['message'] = 'update'
        context['action_url'] = reverse_lazy('Factories:SupplierUpdate', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self, **kwargs):
        if self.object.type == 1:
            messages.success(self.request, "تم تعديل بيانات مورد بنجاح", extra_tags="success")
        else:
            messages.success(self.request, "تم تعديل بيانات مستورد بنجاح", extra_tags="success")
        return reverse('Factories:SupplierList', kwargs={'type': self.object.type})


class SupplierDelete(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = Supplier
    form_class = SupplierDeleteForm
    template_name = 'forms/form_template.html'

    def get_success_url(self):
        return reverse('Factories:SupplierList', kwargs={'type': self.object.type})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object.type == 1:
            context['title'] = 'حذف مورد: ' + str(self.object)
        else:
            context['title'] = 'حذف مستورد: ' + str(self.object)
        context['message'] = 'delete'
        context['action_url'] = reverse_lazy('Factories:SupplierDelete', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        if self.object.type == 1:
            messages.success(self.request, " تم حذف مورد " + str(self.object) + ' بنجاح ', extra_tags="danger")
        else:
            messages.success(self.request, " تم حذف مستورد " + str(self.object) + ' بنجاح ', extra_tags="danger")
        myform = Supplier.objects.get(id=self.kwargs['pk'])
        myform.deleted = 1
        myform.save()
        return redirect(self.get_success_url())


class SupplierRestore(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = Supplier
    form_class = SupplierDeleteForm
    template_name = 'forms/form_template.html'

    def get_success_url(self):
        return reverse('Factories:SupplierTrashList', kwargs={'type': self.object.type})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object.type == 1:
            context['title'] = 'استرجاع مورد: ' + str(self.object)
        else:
            context['title'] = 'استرجاع مستورد: ' + str(self.object)
        context['message'] = 'restore'
        context['action_url'] = reverse_lazy('Factories:SupplierRestore', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        if self.object.type == 1:
            messages.success(self.request, " تم استرجاع مورد " + str(self.object) + ' بنجاح ', extra_tags="dark")
        else:
            messages.success(self.request, " تم استرجاع مستورد " + str(self.object) + ' بنجاح ', extra_tags="dark")
        myform = Supplier.objects.get(id=self.kwargs['pk'])
        myform.deleted = 0
        myform.save()
        return redirect(self.get_success_url())


class SupplierSuperDelete(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = Supplier
    form_class = SupplierDeleteForm
    template_name = 'forms/form_template.html'

    def get_success_url(self):
        return reverse('Factories:SupplierTrashList', kwargs={'type': self.object.type})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object.type == 1:
            context['title'] = 'حذف مورد : ' + str(self.object.id) + 'بشكل نهائي'
        else:
            context['title'] = 'حذف مستورد : ' + str(self.object.id) + 'بشكل نهائي'
        context['message'] = 'super_delete'
        context['action_url'] = reverse_lazy('Factories:SupplierSuperDelete', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        if self.object.type == 1:
            messages.success(self.request, " تم حذف مورد " + str(self.object) + " نهائيا بنجاح ", extra_tags="success")
        else:
            messages.success(self.request, " تم حذف مستورد " + str(self.object) + " نهائيا بنجاح ", extra_tags="success")
        my_form = Supplier.objects.get(id=self.kwargs['pk'])
        my_form.delete()
        return redirect(self.get_success_url())


def SupplierQuantityDetail(request, pk):
    supplier = Supplier.objects.get(id=pk)
    quantity = SupplierQuantity.objects.filter(supplier=supplier)
    quantity_prods = quantity.values_list('product__name', flat=True).distinct()

    form = SupplierQuantityForm()
    form.fields['product'].queryset = Product.objects.filter(deleted=False)

    action_url = reverse_lazy('Factories:AddSupplierQuantity', kwargs={'pk': supplier.id})

    system_info = SystemInformation.objects.all()
    if system_info.count() > 0:
        system_info = system_info.last()
    else:
        system_info = None

    context = {
        'supplier': supplier,
        'quantity': quantity,
        'quantity_prods': quantity_prods,
        'form': form,
        'action_url': action_url,
        'system_info': system_info,
        'date': datetime.now().date(),
    }
    return render(request, 'Supplier/supplier_qunatity.html', context)


def AddSupplierQuantity(request, pk):
    supplier = Supplier.objects.get(id=pk)
    form = SupplierQuantityForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.supplier = supplier
        obj.admin = request.user
        obj.save()
        messages.success(request, " تم اضافة كمية جديدة بنجاح ", extra_tags="success")
    else:
        messages.error(request, " دث خطأ أثناء اضافة الكمية ", extra_tags="danger")
    return redirect('Factories:SupplierQuantity', pk=supplier.id)


def DelSupplierQuantity(request, pk):
    quant = SupplierQuantity.objects.get(id=pk)
    id = quant.supplier.id
    quant.delete()
    messages.success(request, " تم حذف كمية بنجاح ", extra_tags="success")
    return redirect('Factories:SupplierQuantity', pk=id)


def SupplierPaymentDetail(request, pk):
    supplier = Supplier.objects.get(id=pk)
    payment = SupplierPayment.objects.filter(supplier=supplier)

    form = SupplierPaymentForm()
    action_url = reverse_lazy('Factories:AddSupplierPayment', kwargs={'pk': supplier.id})

    system_info = SystemInformation.objects.all()
    if system_info.count() > 0:
        system_info = system_info.last()
    else:
        system_info = None

    context = {
        'supplier': supplier,
        'payment': payment,
        'form': form,
        'action_url': action_url,
        'system_info': system_info,
        'date': datetime.now().date(),
    }
    return render(request, 'Supplier/supplier_payment.html', context)


def AddSupplierPayment(request, pk):
    supplier = Supplier.objects.get(id=pk)
    form = SupplierPaymentForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.supplier = supplier
        obj.admin = request.user
        obj.save()
        messages.success(request, " تم اضافة دفعة جديدة بنجاح ", extra_tags="success")
    else:
        messages.error(request, " دث خطأ أثناء اضافة الدفعة ", extra_tags="danger")
    return redirect('Factories:SupplierPayment', pk=supplier.id)


def DelSupplierPayment(request, pk):
    pay = SupplierPayment.objects.get(id=pk)
    id = pay.supplier.id
    pay.delete()
    messages.success(request, " تم حذف دفعة بنجاح ", extra_tags="success")
    return redirect('Factories:SupplierPayment', pk=id)


def PrintSupplierAll(request, pk):
    supplier = Supplier.objects.get(id=pk)
    system_info = SystemInformation.objects.all()
    if system_info.count() > 0:
        system_info = system_info.last()
    else:
        system_info = None

    quantity = SupplierQuantity.objects.filter(supplier=supplier)
    if quantity:
        count = quantity.aggregate(count=Sum('product_count')).get('count')
        account = quantity.aggregate(account=Sum('total_account')).get('account')
    else:
        count = 0
        account = 0

    payment = SupplierPayment.objects.filter(supplier=supplier)
    if payment:
        total = payment.aggregate(total=Sum('value')).get('total')
    else:
        total = 0

    context = {
        'quantity': quantity,
        'count': count,
        'account': account,
        'payment': payment,
        'total': total,
        'system_info': system_info,
        'date': datetime.now(),
        'user': request.user.username,
        'supplier': supplier,
    }
    html_string = render_to_string('Supplier_Reports/print_supplier_details.html', context)
    html = weasyprint.HTML(string=html_string, base_url=request.build_absolute_uri())
    pdf = html.write_pdf(stylesheets=[weasyprint.CSS('static/assets/css/invoice_pdf.css')], presentational_hints=True)
    response = HttpResponse(pdf, content_type='application/pdf')
    return response