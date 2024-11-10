"""Forms.py"""

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Product, Category

User = get_user_model()

class SignUpForm(UserCreationForm):
# pylint: disable=R0901
    """Signup form class"""
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')
    usable_password = None

    class Meta:
        """gets the required fields"""
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def clean(self):
        """makes the first_name and the last_name required"""
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')

        if not first_name:
            self.add_error('first_name', 'First name is required.')
        if not last_name:
            self.add_error('last_name', 'Last name is required.')

        return cleaned_data

class LoginForm(forms.Form):
    """logins with the username and password"""
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class UserEditForm(forms.ModelForm):
    """edits the form details"""
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')
    user_type = forms.ChoiceField(
        choices=[('customer', 'Customer'), ('admin', 'Admin'), ('superadmin', 'Super Admin')],
        disabled=True,
        required=False
    )
    class Meta:
        """edits the fields"""
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'user_type')

    def __init__(self, *args, **kwargs):
        """doesnt change the username"""
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.is_superuser:
            self.fields['user_type'].initial = 'superadmin'
        self.fields['username'].widget.attrs['readonly'] = True

    def clean_username(self):
        """returns the username"""
        return self.instance.username

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')

        if not first_name:
            self.add_error('first_name', 'First name is required.')
        if not last_name:
            self.add_error('last_name', 'Last name is required.')
        return cleaned_data

class ProductForm(forms.ModelForm):
    """product form"""
    class Meta:
        """meta class defines the fields"""
        model = Product
        fields = ['name', 'category', 'brand', 'image', 'description', 'price', 'stock']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'brand': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class CategoryForm(forms.ModelForm):
    """category form"""
    class Meta:
        """gives the category name"""
        model = Category
        fields = ['name']
