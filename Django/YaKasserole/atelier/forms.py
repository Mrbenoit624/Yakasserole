from django import forms

class ConnectForm(forms.Form):
    #atelier = forms.
    username = forms.CharField(label='Username', max_length=10)
    password = forms.CharField(label='Password',widget=forms.PasswordInput)
