from django import forms
from core.models import Customer, Group, Product

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        exclude = ['user']

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        exclude = ['user']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['user']
