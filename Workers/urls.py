from django.urls import path
from .views import * 

app_name = 'Workers'
urlpatterns = [
    path('worker_list/', WorkerList.as_view(), name="WorkerList"),
    path('trach/',WorkerTrachList.as_view(), name="WorkerTrachList"),
    path('create/',WorkerCreate.as_view(), name="WorkerCreate"),
    path('update/<int:pk>',WorkerUpdate.as_view(), name="WorkerUpdate"),
    path('delete/<int:pk>',WorkerDelete.as_view(), name="WorkerDelete"),
    path('restore/<int:pk>',WorkerRestore.as_view(), name="WorkerRestore"),
    path('superDelete/<int:pk>',WorkerSuperDelete.as_view(), name="WorkerSuperDelete"),
    
    
    
    path('detail/payment/<int:pk>', WorkerPayments.as_view(), name="WorkerPayment"),
    path('detail/payment/<int:pk>/div/', WorkerPayment_div.as_view(), name="WorkerPayment_div"),
    path('payment/create/', WorkerPaymentCreate, name="WorkerPaymentCreate"),
    path('payment/delete/', WorkerPaymentDelete, name="WorkerPaymentDelete"),
    path('payment/update/<int:pk>/', WorkerPaymentUpdate.as_view(), name="WorkerPaymentUpdate"),
    path('payment/print/<int:pk>/', PrintWorkerPayment , name="PrintWorkerPayment"),
    
    
    
    path('detail/attendance/<int:pk>', WorkerAttendances.as_view(), name="WorkerAttendances"),
    path('detail/attendance/<int:pk>/div/', WorkerAttendance_div.as_view(), name="WorkerAttendance_div"),
    path('update/attendance/<int:pk>/', WorkerAttendancesUpdate.as_view(), name="WorkerAttendancesUpdate"),
    path('create/attendnace', WorkerAttendanceCreate, name="WorkerAttendanceCreate"),
    path('delete/attendnace', WorkerAttendanceDelete, name="WorkerAttendanceDelete"),
    path('report/attendance/<int:pk>/', WorkerReports.as_view(), name="WorkerReports"),
    path('attendance/print/<int:pk>/', PrintWorkerAttendance , name="PrintWorkerAttendance"),
    path('productions/print/<int:pk>/', PrintWorkerproductions , name="PrintWorkerproductions"),
    path('all/print/<int:pk>/', PrintWorkerAll , name="PrintWorkerAll"),

    
    

    path('detail/production/<int:pk>', WorkerProductions.as_view(), name="WorkerProduction"),
    path('detail/production/<int:pk>/div/', Worker_Production_div.as_view(), name="WorkerProductions_div"),
    path('create/workerProdduction', WorkerProductionCreate, name="WorkerProductionCreate"),
    path('update/workerProdduction/<int:pk>/', WorkerProductionUpdate.as_view(), name="WorkerProductionUpdate"),
    path('delete/worker_production', WorkerProductionDelete, name="WorkerProductionDelete"),
    
]
    