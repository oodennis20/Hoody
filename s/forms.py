from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

class NewProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user', 'business']

class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        exclude = ['user']

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')