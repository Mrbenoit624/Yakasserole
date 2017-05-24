from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django import template
import datetime

class Commentaire(models.Model):
    Titre = models.CharField(max_length=65)
    Messages = models.TextField()
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

register = template.Library()
@register.filter(name='addcss')
def addcss(field, css):
   return field.as_widget(attrs={"class":css})
