from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Company
from django.utils.translation import gettext_lazy as _

class UserForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username','email', 'password1', 'password2')

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('first_name', 'last_name', 'company_name', 'address', 'phone')
        labels = {
            'first_name': _('first_name'),
            'last_name': _('last_name'),
            'company_name': _('company_name'),
            'address': _('address'),
            'phone': _('phone'),
        }

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)