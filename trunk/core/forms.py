from django import forms
from core.models import Customer, Category, Product, Sale


def make_custom_datefield(f):
    formfield = f.formfield()
    if isinstance(f, models.DateField):
        formfield.widget.format = '%m/%d/%Y'
        formfield.widget.attrs.update({'class':'datePicker', 'readonly':'true'})
    return formfield


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
    formfield_callback = make_custom_datefield
    class Meta:
        model = Sale
        exclude = ['user']
