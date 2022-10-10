import datetime
from django.db.models.aggregates import Sum
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import  LoginRequiredMixin
from django.views.generic import *

from Core.models import SystemInformation
from .forms import *
from django.contrib import messages
import weasyprint
from django.template.loader import render_to_string
from datetime import datetime


class WorkerList(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = Worker
    paginate_by = 12
    template_name = 'Worker/worker_list.html'
    
    def get_queryset(self):
        qureyset = self.model.objects.filter(deleted=False).order_by('-id')
        return qureyset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'list'
        context['title'] = 'قائمة العمال'
        context['icons'] = '<i class="fas fa-shapes"></i>'
        context['page'] = 'active'
        context['count'] = self.model.objects.filter(deleted=False).count()
        return context


class WorkerTrachList(LoginRequiredMixin, ListView):
    login_url = '/auth/login'
    model = Worker
    paginate_by = 12
    template_name = 'Worker/worker_list.html'
    
    def get_queryset(self):
        queyset = self.model.objects.filter(deleted=True).order_by('-id')
        return queyset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'trach'
        context['count'] = self.model.objects.filter(deleted=True).count()
        return context


class WorkerCreate(LoginRequiredMixin, CreateView):
    login_url = '/auth/login/'
    model = Worker
    form_class = WorkerForm
    template_name = 'forms/form_template.html'
    success_url = reverse_lazy('Workers:workerList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'اضافة عامل جديد'
        context['message'] = 'add'
        context['action_url'] = reverse_lazy('Workers:WorkerCreate')
        return context
    
    def get_success_url(self):
        messages.success(self.request, "تم اضافة عامل جديد", extra_tags="success")

        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url
        

class WorkerUpdate(LoginRequiredMixin ,UpdateView):
    login_url = '/auth/login/'
    model = Worker
    form_class = WorkerForm
    template_name = 'forms/form_template.html'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل عامل: ' + str(self.object)
        context['message'] = 'update'
        context['action_url'] = reverse_lazy('Workers:WorkerUpdate', kwargs={'pk': self.object.id})
        return context
    
    def get_success_url(self):
        messages.success(self.request,  "تم تعديل العامل " + str(self.object) + " بنجاح ", extra_tags="success")
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url        
        

class WorkerDelete(LoginRequiredMixin ,UpdateView):
    login_url = '/auth/login/'
    model = Worker
    form_class = WorkerDeleteForm
    template_name = 'forms/form_template.html'
    

    def get_success_url(self):
        return reverse('Workers:WorkerList')
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'نقل العامل الي سلة المهملات: ' + str(self.object)
        context['message'] = 'delete'
        context['action_url'] = reverse_lazy('Workers:WorkerDelete', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        messages.success(self.request, " تم نقل العامل " + str(self.object) + ' الي سلة المهملات بنجاح ' , extra_tags="success")
        myform = Worker.objects.get(id=self.kwargs['pk'])
        myform.deleted = 1
        myform.save()
        return redirect(self.get_success_url())
    
class WorkerRestore(LoginRequiredMixin ,UpdateView):
    login_url = '/auth/login/'
    model = Worker
    form_class = WorkerDeleteForm
    template_name = 'forms/form_template.html'
    

    def get_success_url(self):
        return reverse('Workers:WorkerList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'استرجاع العامل: ' + str(self.object)
        context['message'] = 'restore'
        context['action_url'] = reverse_lazy('Workers:WorkerRestore', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        messages.success(self.request, " تم العامل " + str(self.object) + ' الي القائمة بنجاح ' , extra_tags="success")
        myform = Worker.objects.get(id=self.kwargs['pk'])
        myform.deleted = 0
        myform.save()
        return redirect(self.get_success_url())


class WorkerSuperDelete(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = Worker
    form_class = WorkerDeleteForm
    template_name = 'forms/form_template.html'

    def get_success_url(self):
        return reverse('Workers:WorkerTrachList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'حذف العامل : ' + str(self.object)
        context['message'] = 'super_delete'
        context['action_url'] = reverse_lazy('Workers:WorkerSuperDelete', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        messages.success(self.request, " تم حذف العامل " + str(self.object) + " نهائيا بنجاح ", extra_tags="success")
        my_form = Worker.objects.get(id=self.kwargs['pk'])
        my_form.delete()
        return redirect(self.get_success_url())                      



class WorkerPayments(LoginRequiredMixin, DetailView):
    login_url = '/auth/login/'
    model = Worker
    template_name = 'Worker/worker_payment.html'

    def get_real_count_days(self):
        atta = WorkerAttendance.objects.filter(worker=self.object).order_by('-date', '-id')
        if atta != None:
            val = 0
            for item in atta:
                if item.hour_count == 1:
                    hours = 6
                elif item.hour_count == 2:
                    hours = 8
                elif item.hour_count == 3:
                    hours = 12
                elif item.hour_count == 4:
                    hours = 18
                else:
                    hours = 0
                val = val + hours
            count_days = val
            real_days = count_days / 12
            rest_hours = count_days % 12
        else:
            real_days = 0
            rest_hours = 0
        total = {
            'real_days': int(real_days),
            'rest_hours': int(rest_hours)
        }
        return total

    def get_sum_salary(self, **kwargs):
        worker = Worker.objects.get(id=self.object.id)
        worker_price = worker.day_cost

        count_days = self.get_real_count_days()["real_days"]
        count_hours = self.get_real_count_days()["rest_hours"] / 12
        sum_price = count_days * worker_price
        sum_price2 = count_hours * worker_price
        total = {
            'sum_price': sum_price + sum_price2
        }
        return total
    
    def get_context_data(self, **kwargs):
        queryset = WorkerPayment.objects.filter(worker=self.object)
        payment_sum = queryset.aggregate(price=Sum('price')).get('price')
        context = super().get_context_data(**kwargs)
        context['payment'] = queryset.order_by('-date', '-id')
        context['payment_sum'] = payment_sum
        if self.object.worker_type == 5:
            context['all_cost'] = self.get_sum_salary()
        else:
            total = WorkerProduction.objects.filter(worker=self.object).aggregate(quantity=Sum('quantity')).get('quantity')
            price = self.object.day_cost
            if price and total != None:
                cost = {
                    'sum_price': total * price
                }
            else:
                cost = {
                    'sum_price': 0
                }
            context['all_cost'] = cost
        context['title'] = 'مسحوبات العامل: ' + str(self.object)
        context['form'] = WorkerPaymentForm(self.request.POST or None)
        context['type'] = 'list'
        context['obj'] = self.object
        return context


class WorkerProductions(LoginRequiredMixin, DetailView):
    login_url = '/auth/login/'
    model = Worker 
    template_name = 'Worker/worker_production.html'
    
    def get_context_data(self, **kwargs):
        queryset = WorkerProduction.objects.filter(worker=self.object)
        context = super().get_context_data(**kwargs)
        context['title'] = 'انتاج العامل: ' + str(self.object)
        context['production'] = queryset.order_by('-date', '-id')

        form = WorkerProductionForm(self.request.POST or None)
        form.fields['price'].initial = self.object.day_cost
        context['form'] = form
        context['type']  = 'list'
        
        # summ all quantity
        total = queryset.aggregate(quantity=Sum('quantity')).get('quantity') 
        # day cost for worker
        # price = self.object.day_cost
        # if price and total != None:
        #     cost = total * price
        # else:
        #     cost = 0
        cost = queryset.aggregate(total=Sum('total')).get('total')

        context['total_production'] = total
        context['total'] = cost
        context['obj'] = self.object
        
        return context
        

class Worker_Production_div(LoginRequiredMixin, DetailView):
    login_url = '/auth/login/'
    model = Worker 
    template_name = 'Worker/worker_production_div.html'
    
    def get_context_data(self, **kwargs):
        queryset = WorkerProduction.objects.filter(worker=self.object)
        context = super().get_context_data(**kwargs)
        context['title'] = 'انتاج العامل: ' + str(self.object)
        context['production'] = queryset.order_by('-date', '-id')

        form = WorkerProductionForm(self.request.POST or None)
        form.fields['price'].initial = self.object.day_cost
        context['form'] = form
        context['type'] = 'list'
        
        # summ all quantity
        total = queryset.aggregate(quantity=Sum('quantity')).get('quantity') 
        # day cost for worker
        # price = self.object.day_cost
        # if price and total != None:
        #     cost = total * price
        # else:
        #     cost = 0
        cost = queryset.aggregate(total=Sum('total')).get('total')
            
        context['total_production'] = total
        context['total'] = cost
        context['obj'] = self.object
        
        return context
        
class WorkerProductionUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = WorkerProduction
    form_class = WorkerProductionForm
    template_name = 'forms/form_template.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل  انتاج العامل يوم : ' + str(self.object)
        context['message'] = 'update'
        context['action_url'] = reverse_lazy('Workers:WorkerProductionUpdate', kwargs={'pk': self.object.id})
        return context 

    def get_success_url(self):
        messages.success(self.request, " تم تعديل الانتاج " + str(self.object) + " بنجاح ", extra_tags="success")
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url
           
    
class WorkerPayment_div(LoginRequiredMixin, DetailView):
    login_url = '/auth/login/'
    model = Worker
    template_name = 'Worker/worker_payment_div.html'

    def get_real_count_days(self):
        atta = WorkerAttendance.objects.filter(worker=self.object).order_by('-date', '-id')
        if atta != None:
            val = 0
            for item in atta:
                if item.hour_count == 1:
                    hours = 6
                elif item.hour_count == 2:
                    hours = 8
                elif item.hour_count == 3:
                    hours = 12
                elif item.hour_count == 4:
                    hours = 18
                else:
                    hours = 0
                val = val + hours
            count_days = val
            real_days = count_days / 12
            rest_hours = count_days % 12
        else:
            real_days = 0
            rest_hours = 0
        total = {
            'real_days': int(real_days),
            'rest_hours': int(rest_hours)
        }
        return total

    def get_sum_salary(self, **kwargs):
        worker = Worker.objects.get(id=self.object.id)
        worker_price = worker.day_cost

        count_days = self.get_real_count_days()["real_days"]
        count_hours = self.get_real_count_days()["rest_hours"] / 12
        sum_price = count_days * worker_price
        sum_price2 = count_hours * worker_price
        total = {
            'sum_price': sum_price + sum_price2
        }
        return total

    def get_context_data(self, **kwargs):
        queryset = WorkerPayment.objects.filter(worker=self.object).order_by('-id')
        payment_sum = queryset.aggregate(price=Sum('price')).get('price')
        context = super().get_context_data(**kwargs)
        context['payment'] = queryset.order_by('-date', '-id')
        context['payment_sum'] = payment_sum
        if self.object.worker_type == 5:
            context['all_cost'] = self.get_sum_salary()
        else:
            total = WorkerProduction.objects.filter(worker=self.object).aggregate(quantity=Sum('quantity')).get(
                'quantity')
            price = self.object.day_cost
            if price and total != None:
                cost = {
                    'sum_price': total * price
                }
            else:
                cost = {
                    'sum_price': 0
                }
            context['all_cost'] = cost
        context['title'] = 'مسحوبات العامل: ' + str(self.object)
        context['form'] = WorkerPaymentForm(self.request.POST or None)
        context['type'] = 'list'
        context['obj'] = self.object
        return context



class WorkerPaymentUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = WorkerPayment
    form_class = WorkerPaymentForm
    template_name = 'forms/form_template.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل  مسحوبات يوم : ' + str(self.object)
        context['message'] = 'update'
        context['action_url'] = reverse_lazy('Workers:WorkerPaymentUpdate', kwargs={'pk': self.object.id})
        return context 
    
    def get_success_url(self):
        messages.success(self.request, " تم تعديل المسحوبات " + str(self.object) + " بنجاح ", extra_tags="success")
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url
        
        


def WorkerPaymentCreate(request):
    if request.is_ajax():
        worker_id = request.POST.get('id')
        worker = Worker.objects.get(id=worker_id)
        
        date = request.POST.get('date')
        # admin = request.POST.get('admin')
        # user = User.objects.get(id=admin)
        price = request.POST.get('price')
        
        if worker_id and date and price:
            obj = WorkerPayment()
            obj.worker = worker
            obj.date = date
            obj.admin = request.user
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
    
    
def WorkerProductionCreate(request):
    if request.is_ajax():
        worker_id = request.POST.get('id')
        worker = Worker.objects.get(id=worker_id)
        
        date = request.POST.get('date')
        day = request.POST.get('day')
        quantity = request.POST.get('worker_quantity')
        price = request.POST.get('worker_price')
        total = request.POST.get('worker_total')
        # product = request.POST.get('worker_production')
        
        if worker and date and day and quantity and price and total:
            obj = WorkerProduction()
            obj.admin = request.user
            obj.date = date
            obj.day = day
            obj.quantity = quantity
            obj.price = price
            obj.total = total
            # obj.product = Product.objects.get(id=int(product))
            obj.worker = worker   
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
    
def WorkerPaymentDelete(request):
    if request.is_ajax():
        payment_id = request.POST.get('payment_id')
        obj =  WorkerPayment.objects.get(id=payment_id)
        obj.delete()
        
        if obj:
            response = {
                'msg' : 'Send Successfully'
            }

        return JsonResponse(response)

    
def PrintWorkerPayment(request,pk):
    worker = Worker.objects.get(id=pk)
    system_info = SystemInformation.objects.all()
    if system_info.count() > 0:
        system_info = system_info.last()
    else:
        system_info = None
            
    queryset = WorkerPayment.objects.filter(worker=pk).order_by('-date')
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
        'worker':worker,
    }
    html_string = render_to_string('Worker_Reports/print_worker_payment.html', context)
    html = weasyprint.HTML(string=html_string, base_url=request.build_absolute_uri())
    pdf = html.write_pdf(stylesheets=[weasyprint.CSS('static/assets/css/invoice_pdf.css')], presentational_hints=True)
    response = HttpResponse(pdf, content_type='application/pdf')
    return response    



class WorkerAttendances(LoginRequiredMixin, DetailView):
    login_url = '/auth/login/'
    model = Worker
    template_name = 'Worker/worker_attendance.html'
    
    
    def get_count_days(self):
        atta = WorkerAttendance.objects.filter(worker=self.object).order_by('-date', '-id')
        if atta != None:
            count_days = atta.count()
        else:
            count_days = 0
        total = {
            'count_days': count_days
        }
        return total

    def get_real_count_days(self):
        atta = WorkerAttendance.objects.filter(worker=self.object).order_by('-date', '-id')
        if atta != None:
            val = 0
            for item in atta:
                if item.hour_count == 1:
                    hours = 6
                elif item.hour_count == 2:
                    hours = 8
                elif item.hour_count == 3:
                    hours = 12
                elif item.hour_count == 4:
                    hours = 18
                else:
                    hours = 0
                val = val + hours
            count_days = val
            real_days = count_days / 12
            rest_hours = count_days % 12
        else:
            real_days = 0
            rest_hours = 0
        total = {
            'real_days': int(real_days),
            'rest_hours': int(rest_hours)
        }
        return total

    def get_sum_salary(self, **kwargs):
        worker = Worker.objects.get(id=self.object.id)
        worker_price = worker.day_cost

        count_days = self.get_real_count_days()["real_days"]
        count_hours = self.get_real_count_days()["rest_hours"] / 12
        sum_price = count_days * worker_price
        sum_price2 = count_hours * worker_price
        total = {
            'sum_price': sum_price + sum_price2
        }
        return total

    def get_context_data(self, **kwargs):
        form = WorkerAttendanceForm(self.request.POST or None)
        form.fields['hour_count'].initial = 3
        queryset = WorkerAttendance.objects.filter(worker=self.object)
        context = super().get_context_data(**kwargs)
        context['workers'] = queryset.order_by('-date', '-id')
        context['summary'] = self.get_count_days()
        context['real_summary'] = self.get_real_count_days()
        context['all_cost'] = self.get_sum_salary()
        context['title'] = 'حضور العامل: ' + str(self.object)
        context['form'] = form
        context['type'] = 'list'
        context['obj'] = self.object
        return context
    
    
class WorkerAttendance_div(LoginRequiredMixin, DetailView):
    login_url = '/auth/login/'
    model = Worker
    template_name = 'Worker/worker_attendance_div.html'
    
    def get_count_days(self):
        atta = WorkerAttendance.objects.filter(worker = self.object).order_by('-date', '-id')
        if atta != None:
            count_days =  atta.count()
        else:
            count_days = 0
        total = {
            'count_days' :count_days
        }
        return total

    def get_real_count_days(self):
        atta = WorkerAttendance.objects.filter(worker=self.object).order_by('-date', '-id')
        if atta != None:
            val = 0
            for item in atta:
                if item.hour_count == 1:
                    hours = 6
                elif item.hour_count == 2:
                    hours = 8
                elif item.hour_count == 3:
                    hours = 12
                elif item.hour_count == 4:
                    hours = 18
                else:
                    hours = 0
                val = val + hours
            count_days = val
            real_days = count_days / 12
            rest_hours = count_days % 12
        else:
            real_days = 0
            rest_hours = 0
        total = {
            'real_days': int(real_days),
            'rest_hours': int(rest_hours)
        }
        return total

    def get_sum_salary(self, **kwargs):
        worker = Worker.objects.get(id=self.object.id)
        worker_price = worker.day_cost

        count_days = self.get_real_count_days()["real_days"]
        count_hours = self.get_real_count_days()["rest_hours"] / 12
        sum_price = count_days * worker_price
        sum_price2 = count_hours * worker_price
        total = {
            'sum_price': sum_price + sum_price2
        }
        return total
    
    def get_context_data(self, **kwargs):
        form = WorkerAttendanceForm(self.request.POST or None)
        form.fields['hour_count'].initial = 3
        queryset = WorkerAttendance.objects.filter(worker=self.object)
        context = super().get_context_data(**kwargs)
        context['workers'] = queryset.order_by('-date', '-id')
        context['summary'] = self.get_count_days()
        context['real_summary'] = self.get_real_count_days()
        context['all_cost'] = self.get_sum_salary()
        context['title'] = 'حضور العامل: ' + str(self.object)
        context['form'] = form
        context['type'] = 'list'
        context['obj'] = self.object
        return context
    

def WorkerAttendanceCreate(request):
    if request.is_ajax():
        worker_id = request.POST.get('id')
        
        worker = Worker.objects.get(id=worker_id)
        print(worker)
        
        date = request.POST.get('date')
        day = request.POST.get('day')
        print(date)
        hour_count = request.POST.get('hour_count')
        print(hour_count)
        user = request.user
        print(user)
        
        
        if  date and day and hour_count:
            obj = WorkerAttendance()
            obj.worker = worker
            obj.date = date
            obj.day = day
            obj.hour_count = hour_count
            obj.attend = True
            obj.admin = user
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


class WorkerAttendancesUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = WorkerAttendance
    form_class = WorkerAttendanceForm
    template_name = 'forms/form_template.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل حضور  : ' + str(self.object)
        context['message'] = 'update'
        context['action_url'] = reverse_lazy('Workers:WorkerAttendancesUpdate', kwargs={'pk': self.object.id})
        return context 
    
    def get_success_url(self):
        messages.success(self.request, " تم تعديل الحضور " + str(self.object) + " بنجاح ", extra_tags="success")
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url
    


def WorkerAttendanceDelete(request):
    if request.is_ajax():
        attendance_id = request.POST.get('attendance_id')
        obj =  WorkerAttendance.objects.get(id=attendance_id)
        obj.delete()
        
        if obj:
            response = {
                'msg' : 'Send Successfully'
            }

        return JsonResponse(response)    
    
    
def WorkerProductionDelete(request):
    if request.is_ajax():
        production_id = request.POST.get('worker_Production_id')
        obj =  WorkerProduction.objects.get(id=production_id)
        obj.delete()
        
        if obj:
            response = {
                'msg' : 'Send Successfully'
            }

        return JsonResponse(response)    
            

class WorkerReports(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    form = WorkerPaymentReportForm()
    template_name = 'Worker_Reports/worker_reports.html'
    
   
    def queryset(self):
        if not self.request.GET.get('submit'):
            queryset = None
        else:
            queryset = WorkerAttendance.objects.filter(worker = self.kwargs['pk']).order_by('-date')
            if self.request.GET.get('from_date'):
                queryset = queryset.filter(date__gte = self.request.GET.get('from_date'))
            if self.request.GET.get('to_date'):
                queryset = queryset.filter(date__lte = self.request.GET.get('to_date'))
                                  
        return queryset 
    
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        context['name'] = Worker.objects.get(id=self.kwargs['pk'])
        return context
    
    
def PrintWorkerAttendance(request,pk):
    worker = Worker.objects.get(id=pk)
    system_info = SystemInformation.objects.all()
    if system_info.count() > 0:
        system_info = system_info.last()
    else:
        system_info = None
            
    queryset = WorkerAttendance.objects.filter(worker=pk).order_by('-date')
    if request.GET.get('from_date'):
        queryset = queryset.filter(date__gte = request.GET.get('from_date'))
    if request.GET.get('to_date'):
        queryset = queryset.filter(date__lte = request.GET.get('to_date'))
    
    atta = queryset
    if atta != None:
        val = 0
        for item in atta:
            if item.hour_count == 1:
                hours = 6
            elif item.hour_count == 2:
                hours = 8
            elif item.hour_count == 3:
                hours = 12
            elif item.hour_count == 4:
                hours = 18
            else:
                hours = 0
            val = val + hours
        count_days = val
        real_days = count_days / 12
        rest_hours = count_days % 12
    else:
        real_days = 0
        rest_hours = 0

    context = {
        'queryset':queryset,
        'count_days':  queryset.count,
        'system_info':system_info,
        'date': datetime.now(),
        'user': request.user.username,
        'from_date': request.GET.get('from_date'),
        'to_date': request.GET.get('to_date'),
        'worker':worker,
        'real_days':int(real_days),
        'rest_hours':int(rest_hours),
    }
    html_string = render_to_string('Worker_Reports/print_worker_attendance.html', context)
    html = weasyprint.HTML(string=html_string, base_url=request.build_absolute_uri())
    pdf = html.write_pdf(stylesheets=[weasyprint.CSS('static/assets/css/invoice_pdf.css')], presentational_hints=True)
    response = HttpResponse(pdf, content_type='application/pdf')
    return response

      
def PrintWorkerproductions(request,pk):
    worker = Worker.objects.get(id=pk)
    system_info = SystemInformation.objects.all()
    if system_info.count() > 0:
        system_info = system_info.last()
    else:
        system_info = None
            
    queryset = WorkerProduction.objects.filter(worker=pk).order_by('-date')
    if request.GET.get('from_date'):
        queryset = queryset.filter(date__gte = request.GET.get('from_date'))
    if request.GET.get('to_date'):
        queryset = queryset.filter(date__lte = request.GET.get('to_date'))
    
   
    context = {
        'queryset':queryset,
        'total_productions':  queryset.aggregate(quantity=Sum('quantity')).get('quantity'),
        'total_cost':  queryset.aggregate(total=Sum('total')).get('total'),
        'system_info':system_info,
        'date': datetime.now(),
        'user': request.user.username,
        'from_date': request.GET.get('from_date'),
        'to_date': request.GET.get('to_date'),
        'worker':worker,
    }
    html_string = render_to_string('Worker_Reports/print_worker_productions.html', context)
    html = weasyprint.HTML(string=html_string, base_url=request.build_absolute_uri())
    pdf = html.write_pdf(stylesheets=[weasyprint.CSS('static/assets/css/invoice_pdf.css')], presentational_hints=True)
    response = HttpResponse(pdf, content_type='application/pdf')
    return response


def PrintWorkerAll(request, pk):
    worker = Worker.objects.get(id=pk)
    system_info = SystemInformation.objects.all()
    if system_info.count() > 0:
        system_info = system_info.last()
    else:
        system_info = None

    real_days = 0
    rest_hours = 0
    total_production = 0
    total = 0
    payment_sum = 0
    production = WorkerProduction.objects.filter(worker=pk)
    attendance = WorkerAttendance.objects.filter(worker=pk)
    payment = WorkerPayment.objects.filter(worker=pk)

    if attendance:
        val = 0
        for item in attendance:
            if item.hour_count == 1:
                hours = 6
            elif item.hour_count == 2:
                hours = 8
            elif item.hour_count == 3:
                hours = 12
            elif item.hour_count == 4:
                hours = 18
            else:
                hours = 0
            val = val + hours
        count_days = val
        real_days = int(count_days / 12)
        rest_hours = int(count_days % 12)

        worker_price = worker.day_cost
        count_days = real_days
        count_hours = rest_hours / 12
        sum_price = count_days * worker_price
        sum_price2 = count_hours * worker_price
        total = sum_price + sum_price2

    if production:
        total = production.aggregate(quantity=Sum('quantity')).get('quantity')
        cost = production.aggregate(total=Sum('total')).get('total')
        # price = worker.day_cost
        # if price and total != None:
        #     cost = total * price
        # else:
        #     cost = 0
        total_production = total
        total = cost

    if payment:
        payment_sum = payment.aggregate(price=Sum('price')).get('price')

    context = {
        'system_info': system_info,
        'date': datetime.now(),
        'user': request.user.username,
        'worker': worker,
        'total_production': total_production,
        'total': total,
        'real_days': real_days,
        'rest_hours': rest_hours,
        'payment_sum': payment_sum,
    }
    html_string = render_to_string('Worker_Reports/print_worker_details.html', context)
    html = weasyprint.HTML(string=html_string, base_url=request.build_absolute_uri())
    pdf = html.write_pdf(stylesheets=[weasyprint.CSS('static/assets/css/invoice_pdf.css')], presentational_hints=True)
    response = HttpResponse(pdf, content_type='application/pdf')
    return response