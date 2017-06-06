from django import forms
from django.forms import Widget, Select

class ContactForm(forms.Form):
    mail = forms.EmailField(label='Adresse mail')
    fullname = forms.CharField(label='Nom complet')
    sujet = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)
    file = forms.FileField()

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['mail'].widget.attrs['class'] = 'form-control'
        self.fields['fullname'].widget.attrs['class'] = 'form-control'
        self.fields['sujet'].widget.attrs['class'] = 'form-control'
        self.fields['message'].widget.attrs['class'] = 'form-control'
        self.fields['file'].widget.attrs['class'] = 'form-control'
