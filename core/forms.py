from django import forms
from core.models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        exclude = ['user']
