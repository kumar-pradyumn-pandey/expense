from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import DateInput, TextInput
from django.forms import ModelForm
from .models import *

class LoginForm(forms.Form):
    email = forms.CharField(label="",required=True,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Email'}))
    password = forms.CharField(label="",widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Password'}))
    
    class Meta:
        model = User
        fields = ['email_or_phone','password']

class AddCategoryForm(forms.Form):
    name = forms.CharField(label="", required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Name'}))
    category_choices=[("Incoming","Incoming"),("Outgoing","Outgoing")]
    type = forms.ChoiceField(label="", required=True, choices=category_choices)
    class Meta:
        models = Category
        fields=['name','type']



class EditCategoryForm(forms.ModelForm):
    id = forms.IntegerField()
    name = forms.CharField(label="", required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Name'}))
    category_choices=[("Incoming","Incoming"),("Outgoing","Outgoing")]
    type = forms.ChoiceField(label="", required=True, choices=category_choices)
    class Meta:
        model = Category
        fields = ["id",'name','type']