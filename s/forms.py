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