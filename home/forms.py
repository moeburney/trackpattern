from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class PersonalForm(forms.ModelForm):
    change_password = forms.CharField(label=_("Password"), required=False, widget=forms.PasswordInput,)
    
    class Meta:        
        model = User
        fields = ('first_name','last_name','email')
