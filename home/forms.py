from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.forms.widgets import RadioSelect

class PersonalForm(forms.ModelForm):
    change_password = forms.CharField(label=_("Password"), required=False, widget=forms.PasswordInput, )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

attrs_dict = {'class': 'required'}

class SignupForm(forms.Form):
    username = forms.RegexField(regex=r'^\w+$',
        max_length=30,
        widget=forms.TextInput(attrs=attrs_dict),
        label=_("Username"),
        error_messages={'invalid': _("This value must contain only letters, numbers and underscores.")})
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict,
        maxlength=75)),
        label=_("E-mail"))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
        label=_("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
        label=_("Password (again)"))
    first_name = forms.CharField(max_length=30, label=_("First Name"), )
    last_name = forms.CharField(max_length=30, label=_("Last Name"), )
    question_1 = forms.ChoiceField( widget=RadioSelect(), choices=[[True,'Yes'],[False,'No']],label="""Would you like to sign up to our mailing
list to receive free information about analytics and data driven
marketing?""")
    def clean_username(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.
        
        """
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_("A user with that username already exists."))

    def clean(self):
        """
        Verifiy that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.
        
        """
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields didn't match."))
        return self.cleaned_data
