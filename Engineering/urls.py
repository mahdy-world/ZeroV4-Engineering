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

    path('detail_payment/<int:pk>', CompanyPayments.as_view(), name="CompanyPayments"),
    path('detail_payment_div/<int:pk>', CompanyPayments_div.as_view(), name="CompanyPayments_div"),

    path('company_payment/create/', CompanyPaymentCreate, name="CompanyPaymentCreate"),
    path('company_payment/delete/', CompanyPaymentDelete, name="CompanyPaymentDelete"),

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

    path('detail_payment/<int:pk>', SupplierPayments.as_view(), name="SupplierPayment"),
    path('detail_payment_div/<int:pk>', SupplierPayments_div.as_view(), name="SupplierPayment_div"),

    path('supplier_payment/create/', SupplierPaymentCreate, name="SupplierPaymentCreate"),
    path('supplier_payment/delete/', SupplierPaymentDelete, name="SupplierPaymentDelete"),

    ####################################################################
    # Sheet
    path('sheet_list/', SheetList.as_view(), name="SheetList"),
    path('sheet_trach/', SheetTrashList.as_view(), name="SheetTrashList"),
    path('sheet_create/', SheetCreate.as_view(), name="SheetCreate"),
    path('sheet_update/<int:pk>', SheetUpdate.as_view(), name="SheetUpdate"),
    path('sheet_delete/<int:pk>', SheetDelete.as_view(), name="SheetDelete"),
    path('sheet_restore/<int:pk>', SheetRestore.as_view(), name="SheetRestore"),
    path('sheet_superDelete/<int:pk>', SheetSuperDelete.as_view(), name="SheetSuperDelete"),
    path('sheet_detail/<int:pk>/', SheetDetail, name="SheetDetail"),
    path('AddSheetBon/<int:pk>/', AddSheetBon, name="AddSheetBon"),
    path('DelSheetBon/<int:pk>/', DelSheetBon, name="DelSheetBon"),

    ####################################################################

    # more
    path('company_sheet/<int:pk>', CompanySheet.as_view(), name="CompanySheet"),
    path('geo_sheet/<int:pk>', GeoSheet.as_view(), name="GeoSheet"),
    path('supplier_sheet/<int:pk>', SupplierSheet.as_view(), name="SupplierSheet"),

    path('company_bon/<int:pk>', CompanyBon.as_view(), name="CompanyBon"),
    path('geo_bon/<int:pk>', GeoBon.as_view(), name="GeoBon"),
    path('supplier_bon/<int:pk>', SupplierBon.as_view(), name="SupplierBon"),

    path('company_profit/<int:pk>', CompanyProfit.as_view(), name="CompanyProfit"),
    path('geo_profit/<int:pk>', GeoProfit.as_view(), name="GeoProfit"),
    path('supplier_profit/<int:pk>', SupplierProfit.as_view(), name="SupplierProfit"),

    path('months_profit/', MonthsProfit, name="MonthsProfit"),
]
