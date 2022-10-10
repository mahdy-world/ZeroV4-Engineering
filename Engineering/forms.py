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
            'active': forms.CheckboxInput(attrs={'class':'form-control'}),
        }

class GeoPlaceDeleteForm(forms.ModelForm):
    class Meta:
        fields = ['deleted']
        model = GeoPlace
        widgets = {
            'deleted': forms.HiddenInput()
        }