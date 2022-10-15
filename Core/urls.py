from django.urls import path 
from . import views

app_name = 'Core'
urlpatterns = [
    path('', views.Index, name='index'),
    path('systemInfoCreate/', views.SystemInfoCreate.as_view(), name='SystemInfoCreate'),
    path('systemInfoUpdate/<int:pk>/', views.SystemInfoUpdate.as_view(), name='SystemInfoUpdate'),
    path('company_search/', views.CompanySearch.as_view(), name='CompanySearch'),
    path('supplier_search/', views.SupplierSearch.as_view(), name='SupplierSearch'),
    path('geoplace_search/', views.GeoPlaceSearch.as_view(), name='GeoPlaceSearch'),
    path('company_geoplace_search/', views.CompanyGeosSearch.as_view(), name='CompanyGeosSearch'),
]
