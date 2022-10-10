from django.urls import path
from .views import * 

app_name = 'Engineering'
urlpatterns = [
    path('com_list/', CompanyList.as_view(), name="CompanyList"),
    path('com_trach/', CompanyTrachList.as_view(), name="CompanyTrachList"),
    path('com_create/', CompanyCreate.as_view(), name="CompanyCreate"),
    path('com_update/<int:pk>', CompanyUpdate.as_view(), name="CompanyUpdate"),
    path('com_delete/<int:pk>', CompanyDelete.as_view(), name="CompanyDelete"),
    path('com_restore/<int:pk>', CompanyRestore.as_view(), name="CompanyRestore"),
    path('com_superDelete/<int:pk>', CompanySuperDelete.as_view(), name="CompanySuperDelete"),

    ####################################################################

    path('geo_list/', GeoPlaceList.as_view(), name="GeoPlaceList"),
    path('geo_trach/', GeoPlaceTrachList.as_view(), name="GeoPlaceTrachList"),
    path('geo_create/', GeoPlaceCreate.as_view(), name="GeoPlaceCreate"),
    path('geo_update/<int:pk>', GeoPlaceUpdate.as_view(), name="GeoPlaceUpdate"),
    path('geo_delete/<int:pk>', GeoPlaceDelete.as_view(), name="GeoPlaceDelete"),
    path('geo_restore/<int:pk>', GeoPlaceRestore.as_view(), name="GeoPlaceRestore"),
    path('geo_superDelete/<int:pk>', GeoPlaceSuperDelete.as_view(), name="GeoPlaceSuperDelete"),
]
