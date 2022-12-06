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

    path('detail_payment_com/<int:pk>', CompanyPayments.as_view(), name="CompanyPayments"),
    path('detail_payment_div_com/<int:pk>', CompanyPayments_div.as_view(), name="CompanyPayments_div"),

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
    path('geo_price_history/<int:pk>', GeoPlacePriceHistoryList, name="GeoPlacePriceHistoryList"),

    ####################################################################
    # supplier
    path('supplier_list/', SupplierList.as_view(), name="SupplierList"),
    path('supplier_trach/', SupplierTrachList.as_view(), name="SupplierTrachList"),
    path('supplier_create/', SupplierCreate.as_view(), name="SupplierCreate"),
    path('supplier_update/<int:pk>', SupplierUpdate.as_view(), name="SupplierUpdate"),
    path('supplier_delete/<int:pk>', SupplierDelete.as_view(), name="SupplierDelete"),
    path('supplier_restore/<int:pk>', SupplierRestore.as_view(), name="SupplierRestore"),
    path('supplier_superDelete/<int:pk>', SupplierSuperDelete.as_view(), name="SupplierSuperDelete"),

    path('detail_payment_sup/<int:pk>', SupplierPayments.as_view(), name="SupplierPayment"),
    path('detail_payment_div_sup/<int:pk>', SupplierPayments_div.as_view(), name="SupplierPayment_div"),

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
    path('sheet_bon_update/<int:pk>', SheetBonUpdate.as_view(), name="SheetBonUpdate"),
    path('get_company_geos/', get_company_geos, name="get_company_geos"),

    ####################################################################

    # more
    path('company_sheet/<int:pk>', CompanySheet, name="CompanySheet"),
    path('geo_sheet/<int:pk>', GeoSheet, name="GeoSheet"),
    path('supplier_sheet/<int:pk>', SupplierSheet, name="SupplierSheet"),

    path('company_bon/<int:pk>', CompanyBon, name="CompanyBon"),
    path('geo_bon/<int:pk>', GeoBon, name="GeoBon"),
    path('supplier_bon/<int:pk>', SupplierBon, name="SupplierBon"),

    path('company_profit/<int:pk>', CompanyProfit, name="CompanyProfit"),
    path('geo_profit/<int:pk>', GeoProfit, name="GeoProfit"),
    path('supplier_profit/<int:pk>', SupplierProfit, name="SupplierProfit"),

    path('months_profit/', MonthsProfit, name="MonthsProfit"),
    path('bons_reports/', BonsReports, name="bons_reports"),

    ###################################################################

    # Supplier Reoprt
    path('supplier_report/<int:pk>', SupplierReport, name="SupplierReport"),
    path('supplier_report_show/<int:pk>', SupplierReportShow, name="SupplierReportShow"),
    # Company Reoprt
    path('company_report/<int:pk>', CompanyReport, name="CompanyReport"),
    path('company_report_show/<int:pk>', CompanyReportShow, name="CompanyReportShow"),
    # Geo Reoprt
    path('geo_report/<int:pk>', GeoReport, name="GeoReport"),
    path('geo_report_show/<int:pk>', GeoReportShow, name="GeoReportShow"),

]
