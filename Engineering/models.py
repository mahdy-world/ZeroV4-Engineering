from django.db import models
from Auth.models import User
from datetime import date
from datetime import datetime
# Create your models here.

class Company(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الاضافة")
    name = models.CharField(max_length=50, verbose_name="اسم الشركة")
    address = models.CharField(null=True, blank=True, max_length=100, verbose_name="العنوان")
    phone = models.CharField(null=True, blank=True, max_length=12, verbose_name="رقم الهاتف")
    active = models.BooleanField(default=True, verbose_name="نشطة")
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class GeoPlace(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الاضافة")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="الشركة المسؤولة")
    name = models.CharField(max_length=50, verbose_name="اسم الموقع")
    address = models.CharField(null=True, blank=True, max_length=100, verbose_name="العنوان")
    phone = models.CharField(null=True, blank=True, max_length=12, verbose_name="رقم الهاتف")
    price = models.FloatField(default=0.0, verbose_name='سعر الموقع')
    material_price = models.FloatField(default=0.0, verbose_name='سعر الخامة')
    active = models.BooleanField(default=True, verbose_name="نشط")
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class GeoPlacePriceHistory(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الاضافة")
    geo = models.ForeignKey(GeoPlace, on_delete=models.CASCADE, verbose_name="الموقع")
    old_price = models.FloatField(default=0.0, verbose_name='السعر القديم')
    new_price = models.FloatField(default=0.0, verbose_name='السعر الجديد')
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="المسئول")

    def __str__(self):
        return self.geo.name


class GeoPlaceMaterialPriceHistory(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الاضافة")
    geo = models.ForeignKey(GeoPlace, on_delete=models.CASCADE, verbose_name="الموقع")
    old_price = models.FloatField(default=0.0, verbose_name='السعر القديم')
    new_price = models.FloatField(default=0.0, verbose_name='السعر الجديد')
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="المسئول")

    def __str__(self):
        return self.geo.name


class Supplier(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الاضافة")
    name = models.CharField(max_length=50, verbose_name="اسم المورد")
    phone = models.CharField(max_length=12, null=True, blank=True, verbose_name="رقم الهاتف")
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Sheet(models.Model):
    title = models.CharField(max_length=50, verbose_name="عنوان الشيت")
    date = models.DateField(default=datetime.today(), verbose_name="تاريخ الاضافة")
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, verbose_name="المورد")
    bons = models.IntegerField(default=0, null=True, blank=True, verbose_name="البونات")
    quantity = models.FloatField(default=0, null=True, blank=True, verbose_name="الكميات")
    quantity_discount = models.FloatField(default=0.0, verbose_name="خصم")
    quantity_after_discount = models.FloatField(default=0.0, verbose_name="بعد الخصم")
    quantity_diff = models.FloatField(default=0.0, verbose_name="فرق التكعيب")
    total = models.FloatField(default=0, null=True, blank=True, verbose_name="حساب المورد")
    overall = models.FloatField(default=0, null=True, blank=True, verbose_name="حسابي")
    loads_value = models.FloatField(default=0, null=True, blank=True, verbose_name="قيمة العهد")
    supplier_value = models.FloatField(default=0, null=True, blank=True, verbose_name="الصافي للمورد")
    profit = models.FloatField(default=0, null=True, blank=True, verbose_name="الربح")
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="المسئول")
    deleted = models.BooleanField(default=False, verbose_name="حذف")

    def __str__(self):
        return self.title


class Bon(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الاضافة")
    date = models.DateField(default=datetime.today(), verbose_name="التاريخ")
    bon_number = models.CharField(max_length=50, verbose_name="رقم البون")
    car_number = models.CharField(max_length=50, verbose_name="رقم الشاحنة", null=True)
    car_owner = models.CharField(max_length=100, verbose_name="صاحب االشاحنة", null=True)
    kassara = models.CharField(max_length=100, verbose_name="اسم الكسارة", null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="الشركة", null=True)
    geo_place = models.ForeignKey(GeoPlace, on_delete=models.CASCADE, verbose_name="الموقع")
    sheet = models.ForeignKey(Sheet, on_delete=models.CASCADE, verbose_name="الشيت")
    bon_quantity = models.FloatField(default=0.0, verbose_name="الكمية")
    bon_quantity_discount = models.FloatField(default=0.0, verbose_name="خصم كمية")
    bon_quantity_after_discount = models.FloatField(default=0.0, verbose_name="بعد الخصم")
    bon_quantity_diff = models.FloatField(default=0.0, verbose_name="فرق التكعيب")
    bon_price = models.FloatField(default=0.0, verbose_name="السعر")
    bon_total = models.FloatField(default=0.0, null=True, blank=True, verbose_name="الاجمالي للمورد")
    material_price = models.FloatField(default=0.0, null=True, blank=True, verbose_name="سعر الخامة")
    material_total = models.FloatField(default=0.0, null=True, blank=True, verbose_name="اجمالي الخامة")
    geo_price = models.FloatField(default=0.0, null=True, blank=True, verbose_name="سعر الموقع")
    bon_overall = models.FloatField(default=0.0, null=True, blank=True, verbose_name="الحساب عند الشركة")
    profit = models.FloatField(default=0.0, null=True, blank=True, verbose_name="الربح من الكمية")
    diff_profit = models.FloatField(default=0.0, null=True, blank=True, verbose_name="ربح فرق التكعيب")
    total_profit = models.FloatField(default=0.0, null=True, blank=True, verbose_name="اجمالي الربح")
    load_value = models.FloatField(default=0.0, verbose_name="العهدة", null=True)
    supplier_value = models.FloatField(default=0.0, verbose_name="الصافي للمورد", null=True)
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="المسئول")

    def __str__(self):
        return self.bon_number



# Supplier Payment
class SupplierPayment(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الاضافة")
    cash_amount = models.FloatField(default=0, verbose_name="القيمة النقدية", null=True)
    desc = models.CharField(max_length=250, verbose_name="الوصف/السبب", null=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, verbose_name="المورد")
    admin = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="المسئول")
    payment_date = models.DateField(null=True, verbose_name="التاريخ", default=date.today)

    def __str__(self):
        return self.supplier.name


# Company Payment
class CompanyPayment(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الاضافة")
    cash_amount = models.FloatField(default=0, verbose_name="القيمة النقدية", null=True)
    desc = models.CharField(max_length=250, verbose_name="الوصف/السبب", null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="الشركة")
    geo_place = models.ForeignKey(GeoPlace, on_delete=models.CASCADE, verbose_name="الموقع", null=True)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="المسئول")
    payment_date = models.DateField(null=True, verbose_name="التاريخ", default=date.today)

    def __str__(self):
        return self.company.name