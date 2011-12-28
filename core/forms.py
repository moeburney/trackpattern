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

    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('user_id', None)
        super(SaleForm, self).__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.filter(user__id=user_id)
        self.fields['customer'].queryset = Customer.objects.filter(user__id=user_id)
        self.fields['marketing_source'].queryset = Campaign.objects.filter(user__id=user_id)


class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        exclude = ['user']
