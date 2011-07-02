from django import forms
from core.models import Customer, Category, Product, Sale, Campaign

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        exclude = ['user']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ['user']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['user']

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        exclude = ['user']

class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        exclude = ['user']
