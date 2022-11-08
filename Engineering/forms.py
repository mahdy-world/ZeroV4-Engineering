from django import forms
from .models import *


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        exclude = ['deleted', ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'active': forms.CheckboxInput(attrs={'class':'form-control'}),
        }

class CompanyDeleteForm(forms.ModelForm):
    class Meta:
        fields = ['deleted']
        model = Company
        widgets = {
            'deleted': forms.HiddenInput()
        }


class GeoPlaceForm(forms.ModelForm):
    class Meta:
        model = GeoPlace
        exclude = ['deleted', ]
        widgets = {
            'company': forms.Select(attrs={'class': 'form-control', 'id': 'company', 'style': 'width:100%'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'min':0}),
            'active': forms.CheckboxInput(attrs={'class':'form-control'}),
        }

class GeoPlaceDeleteForm(forms.ModelForm):
    class Meta:
        fields = ['deleted']
        model = GeoPlace
        widgets = {
            'deleted': forms.HiddenInput()
        }


# create supplier form
class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        exclude = ['deleted']
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'phone': forms.TextInput(attrs={'class':'form-control', 'min':0}),
        }

# delete supplier form
class SupplierFormDelete(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['deleted']
        widgets = {
            'deleted': forms.HiddenInput()
        }


# create supplier form
class SheetForm(forms.ModelForm):
    class Meta:
        model = Sheet
        exclude = ['deleted', 'admin', 'profit']
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'date': forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
            'company': forms.Select(attrs={'class':'form-control', 'id':'comapny_sheet', 'style': 'width:100%'}),
            'supplier': forms.Select(attrs={'class':'form-control', 'id':'supplier_sheet', 'style': 'width:100%'}),
        }

# delete supplier form
class SheetFormDelete(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['deleted']
        widgets = {
            'deleted': forms.HiddenInput()
        }

class BonForm(forms.ModelForm):
    class Meta:
        model = Bon
        fields = ['date', 'bon_number', 'car_number', 'car_owner', 'geo_place', 'bon_quantity', 'bon_price']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'bon_number': forms.TextInput(attrs={'class': 'form-control'}),
            'car_number': forms.TextInput(attrs={'class': 'form-control', }),
            'car_owner': forms.TextInput(attrs={'class': 'form-control',}),
            'geo_place': forms.Select(attrs={'class': 'form-control', 'id':'geo_place_bon',}),
            'bon_quantity': forms.NumberInput(attrs={'class': 'form-control', 'min':0 }),
            'bon_price': forms.NumberInput(attrs={'class': 'form-control', 'min':0}),
        }

# Supplier Pyament Create Form
class SupplierPaymentForm(forms.ModelForm):
    class Meta:
        model = SupplierPayment
        fields = ['cash_amount', 'admin', 'payment_date']
        widgets = {
            'payment_date': forms.TextInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'تاريخ السحب...', 'id': 'payment_date'}),
            'cash_amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'القيمة النقدية...', 'id': 'cash_amount', 'min':0}),
            'admin': forms.Select(attrs={'class': 'form-control', 'placeholder': 'المسئول...', 'id': 'admin'}),
        }


# Company Pyament Create Form
class CompanyPaymentForm(forms.ModelForm):
    class Meta:
        model = CompanyPayment
        fields = ['cash_amount', 'admin', 'payment_date']
        widgets = {
            'payment_date': forms.TextInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'تاريخ السحب...', 'id': 'payment_date'}),
            'cash_amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'القيمة النقدية...', 'id': 'cash_amount', 'min':0}),
            'admin': forms.Select(attrs={'class': 'form-control', 'placeholder': 'المسئول...', 'id': 'admin'}),
        }
