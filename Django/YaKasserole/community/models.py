from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

class Commentaire(models.Model):
    Titre = models.CharField(max_length=65)
    Messages = models.TextField()
    user_id = models.ForeignKey('auth.User', on_delete=models.CASCADE)

class Chef(models.Model):
    user_id = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    ateliers = models.ForeignKey(Atelier, on_delete=models.CASCADE)

