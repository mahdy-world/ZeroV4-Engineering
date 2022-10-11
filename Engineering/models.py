from django.db import models
from Auth.models import User
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
    price = models.FloatField(default=0.0, verbose_name='السعر')
    active = models.BooleanField(default=True, verbose_name="نشط")
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class GeoPlacePriceHistory(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الاضافة")
    geo = models.ForeignKey(GeoPlace, on_delete=models.CASCADE, verbose_name="الموقع")
    old_price = models.FloatField(default=0.0, verbose_name='السعر القديم')
    new_price = models.FloatField(default=0.0, verbose_name='السعر الجديد')
    admin = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name="المسئول")

    def __str__(self):
        return self.geo.name


class Supplier(models.Model):
    name = models.CharField(max_length=50, verbose_name="اسم المورد")
    phone = models.CharField(max_length=12, null=True, blank=True, verbose_name="رقم الهاتف")
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Sheet(models.Model):
    title = models.CharField(max_length=50, verbose_name="عنوان الشيت")
    date = models.DateField(default=datetime.today(), verbose_name="تاريخ الاضافة")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="الشركة")
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, verbose_name="المورد")
    admin = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name="المسئول")

    def __str__(self):
        return self.title


class Bon(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الاضافة")
    date = models.DateField(default=datetime.today(), verbose_name="التاريخ")
    bon_number = models.CharField(max_length=50, verbose_name="رقم البون")
    car_number = models.CharField(max_length=50, verbose_name="رقم الشاحنة")
    car_owner = models.CharField(max_length=50, verbose_name="صاحب االشاحنة")
    geo_place = models.ForeignKey(GeoPlace, on_delete=models.CASCADE, verbose_name="الموقع")
    sheet = models.ForeignKey(Sheet, on_delete=models.CASCADE, verbose_name="الشيت")
    bon_quantity = models.FloatField(default=0.0, verbose_name="الكمية")
    bon_price = models.FloatField(default=0.0, verbose_name="السعر")
    bon_total = models.FloatField(null=True, blank=True, verbose_name="الاجمالي")
    geo_price = models.FloatField(null=True, blank=True, verbose_name="سعر الموقع")
    profit = models.FloatField(null=True, blank=True, verbose_name="الربح")
    total_profit = models.FloatField(null=True, blank=True, verbose_name="اجمالي الربح")
    admin = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name="المسئول")

    def __str__(self):
        return self.bon_number
