from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Company, Product, ProductCategory
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError
from django.core.validators import EMPTY_VALUES



class UserForm(UserCreationForm):
    email = forms.EmailField(max_length=100, help_text=_('Required. Enter a valid email address.'))
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }

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
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    # def clean(self):
    #     cleaned_data = super().clean()
    #     username = cleaned_data.get("username")
    #     password = cleaned_data.get("password")

    #     if not username or not password:
    #         raise forms.ValidationError("Both username and password are required.")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = _('username')
        self.fields['password'].label = _('login password')



class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'product_category']
        
        labels = {
            'product_name': _('product_name'),
            'product_category': _('product_category'),
        }
        
        error_messages = {
            'product_name': {'required': _('Please fill out this field.')},
            'product_category': {'required': _('Please choose one category.')},
        }

    

