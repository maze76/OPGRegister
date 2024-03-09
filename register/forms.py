from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Company
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError
from django.core.validators import EMPTY_VALUES


# def validate_email_contains_at(value):
#     if '@' not in value:
#         raise ValidationError(_('Email must contain @ symbol.'))
    

def validate_not_empty(value):
    if value in EMPTY_VALUES:
        raise forms.ValidationError(_("This field is required."))

def validate_numeric(value):
    if not value.isdigit():
        raise ValidationError(_('Phone number must contain only numeric characters.'))


class UserForm(UserCreationForm):
    email = forms.EmailField(max_length=100, help_text=_('Required. Enter a valid email address.'))

    class Meta:
        model = User
        fields = ('username','email', 'password1', 'password2')
        labels = {
            'username': _('username'),
            'email': _('email'),
            'password1': _('password1'),
            'password2': _('password2'),
        }
        error_messages = {
            'username': {'required': _('Please fill out this field.')},
            'email': {'required': _('Please fill out this field.')},
            'password1': {'required': _('Please fill out this field.')},
            'password2': {'required': _('Please fill out this field.')},
        }


class CompanyForm(forms.ModelForm):
    # first_name = forms.CharField(error_messages={'required': _('Please fill out this field.')})

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
        error_messages = {
            'first_name': {'required': _('Please fill out this field.')},
            'last_name': {'required': _('Please fill out this field.')},
            'company_name': {'required': _('Please fill out this field.')},
            'address': {'required': _('Please fill out this field.')},
            'phone': {'required': _('Please fill out this field.')},
        }

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)