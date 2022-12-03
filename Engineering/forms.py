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
            'material_price': forms.NumberInput(attrs={'class': 'form-control', 'min':0}),
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
        fields = ['title', 'date', 'supplier']
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'date': forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
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
        fields = ['date', 'bon_number', 'car_number', 'car_owner', 'kassara', 'company', 'geo_place',
                  'bon_quantity', 'bon_quantity_discount', 'bon_quantity_diff', 'bon_price', 'load_value',
                  ]
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'bon_number': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'car_number': forms.TextInput(attrs={'class': 'form-control', }),
            'car_owner': forms.TextInput(attrs={'class': 'form-control',}),
            'kassara': forms.TextInput(attrs={'class': 'form-control',}),
            'company': forms.Select(attrs={'class': 'form-control', 'id':'company_bon', 'style': 'width:100%'}),
            'geo_place': forms.Select(attrs={'class': 'form-control', 'id':'geo_place_bon', 'style': 'width:100%'}),
            'bon_quantity': forms.NumberInput(attrs={'class': 'form-control', 'min':0 }),
            'bon_quantity_discount': forms.NumberInput(attrs={'class': 'form-control', 'min':0 }),
            'bon_quantity_diff': forms.NumberInput(attrs={'class': 'form-control', 'min':0 }),
            'bon_price': forms.NumberInput(attrs={'class': 'form-control', 'min':0}),
            'load_value': forms.NumberInput(attrs={'class': 'form-control', 'min':0}),
        }

    def __init__(self, *args, **kwargs):
        super(BonForm, self).__init__(*args, **kwargs)
        self.fields['car_number'].required = False
        self.fields['car_owner'].required = False
        self.fields['kassara'].required = False
        self.fields['bon_quantity_discount'].required = False
        self.fields['bon_quantity_diff'].required = False
        self.fields['load_value'].required = False


# Supplier Pyament Create Form
class SupplierPaymentForm(forms.ModelForm):
    class Meta:
        model = SupplierPayment
        fields = ['cash_amount', 'admin', 'payment_date', 'desc']
        widgets = {
            'desc': forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'placeholder': 'الوصف/السبب...', 'id': 'payment_desc'}),
            'payment_date': forms.TextInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'تاريخ السحب...', 'id': 'payment_date'}),
            'cash_amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'القيمة النقدية...', 'id': 'cash_amount', 'min':1}),
            'admin': forms.Select(attrs={'class': 'form-control', 'placeholder': 'المسئول...', 'id': 'admin'}),
        }

    def __init__(self, *args, **kwargs):
        super(SupplierPaymentForm, self).__init__(*args, **kwargs)
        self.fields['desc'].required = False


# Company Pyament Create Form
class CompanyPaymentForm(forms.ModelForm):
    class Meta:
        model = CompanyPayment
        fields = ['cash_amount', 'geo_place', 'admin', 'payment_date', 'desc']
        widgets = {
            'desc': forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'placeholder': 'الوصف/السبب...', 'id': 'payment_desc'}),
            'payment_date': forms.TextInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'تاريخ السحب...', 'id': 'payment_date'}),
            'cash_amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'القيمة النقدية...', 'id': 'cash_amount', 'min':1}),
            'geo_place': forms.Select(attrs={'class': 'form-control', 'id': 'geo_place', 'style': 'width:100%'}),
            'admin': forms.Select(attrs={'class': 'form-control', 'placeholder': 'المسئول...', 'id': 'admin'}),
        }

    def __init__(self, *args, **kwargs):
        super(CompanyPaymentForm, self).__init__(*args, **kwargs)
        self.fields['geo_place'].required = False
        self.fields['desc'].required = False


class ReportForm(forms.Form):
    from_date1 = forms.DateField(widget=forms.DateInput(attrs={
        'type': 'Date',
        'name': 'from_date1',
        'id': 'from_date1',
        'class': 'form-control'}),
        label = 'البونات والعهد من'
    )

    to_date1 = forms.DateField(widget=forms.DateInput(attrs={
        'type': 'Date',
        'name': 'to_date1',
        'id': 'to_date1',
        'class': 'form-control'}),
        label = 'الي'
    )

    from_date2 = forms.DateField(widget=forms.DateInput(attrs={
        'type': 'Date',
        'name': 'from_date2',
        'id': 'from_date2',
        'class': 'form-control'}),
        label='المسحوبات من'
    )

    to_date2 = forms.DateField(widget=forms.DateInput(attrs={
        'type': 'Date',
        'name': 'to_date2',
        'id': 'to_date2',
        'class': 'form-control'}),
        label='الي'
    )

    def __init__(self, *args, **kwargs):
        super(ReportForm, self).__init__(*args, **kwargs)
        self.fields['from_date1'].required = False
        self.fields['to_date1'].required = False
        self.fields['from_date2'].required = False
        self.fields['to_date2'].required = False