from django.urls import path
from .views import * 

app_name = 'Engineering'
urlpatterns = [
    # Company
    path('com_list/', CompanyList.as_view(), name="CompanyList"),
    path('com_trach/', CompanyTrachList.as_view(), name="CompanyTrachList"),
    path('com_create/', CompanyCreate.as_view(), name="CompanyCreate"),
    path('com_update/<int:pk>', CompanyUpdate.as_view(), name="CompanyUpdate"),
    path('com_delete/<int:pk>', CompanyDelete.as_view(), name="CompanyDelete"),
    path('com_restore/<int:pk>', CompanyRestore.as_view(), name="CompanyRestore"),
    path('com_superDelete/<int:pk>', CompanySuperDelete.as_view(), name="CompanySuperDelete"),

    ####################################################################
    # GeoPlace
    path('geo_list/', GeoPlaceList.as_view(), name="GeoPlaceList"),
    path('geo_trach/', GeoPlaceTrachList.as_view(), name="GeoPlaceTrachList"),
    path('geo_create/', GeoPlaceCreate.as_view(), name="GeoPlaceCreate"),
    path('geo_update/<int:pk>', GeoPlaceUpdate.as_view(), name="GeoPlaceUpdate"),
    path('geo_delete/<int:pk>', GeoPlaceDelete.as_view(), name="GeoPlaceDelete"),
    path('geo_restore/<int:pk>', GeoPlaceRestore.as_view(), name="GeoPlaceRestore"),
    path('geo_superDelete/<int:pk>', GeoPlaceSuperDelete.as_view(), name="GeoPlaceSuperDelete"),
    path('geo_price_history/<int:pk>', GeoPlacePriceHistoryList.as_view(), name="GeoPlacePriceHistoryList"),

    ####################################################################
    # supplier
    path('supplier_list/', SupplierList.as_view(), name="SupplierList"),
    path('supplier_trach/', SupplierTrachList.as_view(), name="SupplierTrachList"),
    path('supplier_create/', SupplierCreate.as_view(), name="SupplierCreate"),
    path('supplier_update/<int:pk>', SupplierUpdate.as_view(), name="SupplierUpdate"),
    path('supplier_delete/<int:pk>', SupplierDelete.as_view(), name="SupplierDelete"),
    path('supplier_restore/<int:pk>', SupplierRestore.as_view(), name="SupplierRestore"),
    path('supplier_superDelete/<int:pk>', SupplierSuperDelete.as_view(), name="SupplierSuperDelete"),

    ####################################################################
    # Sheet
    path('sheet_list/', SheetList.as_view(), name="SheetList"),
    path('sheet_trach/', SheetTrashList.as_view(), name="SheetTrashList"),
    path('sheet_create/', SheetCreate.as_view(), name="SheetCreate"),
    path('sheet_update/<int:pk>', SheetUpdate.as_view(), name="SheetUpdate"),
    path('sheet_delete/<int:pk>', SheetDelete.as_view(), name="SheetDelete"),
    path('sheet_restore/<int:pk>', SheetRestore.as_view(), name="SheetRestore"),
    path('sheet_superDelete/<int:pk>', SheetDelete.as_view(), name="SheetDelete"),

    ####################################################################
]
