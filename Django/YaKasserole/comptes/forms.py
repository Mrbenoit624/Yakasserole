from django import forms

#from .models import Post
from django.contrib.auth.models import User
from django import forms

class ConnectForm(forms.Form):
    username = forms.CharField(label='Username', max_length=10)
    password = forms.CharField(label='Password',widget=forms.PasswordInput)

