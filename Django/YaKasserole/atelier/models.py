from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.contrib.auth.models import User
from django.utils import timezone
from community.models import Commentaire
import datetime

class Theme(models.Model):
    Name = models.CharField(max_length=65)
    def __str__(self): return self.Name

class Lieu(models.Model):
    Nom = models.CharField(max_length=65)
    Adresse = models.CharField(max_length=65)
    Telephone = models.CharField(max_length=65)
    CodePostal = models.PositiveIntegerField(default=0)
    Ville = models.CharField(max_length=65)
    def __str__(self): return self.Nom

class Participant(models.Model):
    prenom = models.CharField(max_length=65, blank=False)
    nom = models.CharField(max_length=65, blank=False)
    def __str__(self): return self.first_name + self.last_name

class Atelier(models.Model):
    Nom = models.CharField(max_length=65)
    Lieux = models.ManyToManyField(
        Lieu,
        through='Ateliers_Lieux',
        through_fields=('ateliers', 'lieux'),
    )
    Themes = models.ManyToManyField(
        Theme,
        through='Ateliers_themes',
        through_fields=('ateliers', 'themes'),
    )
    Chef = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    Prix = models.DecimalField(max_digits=8, decimal_places=2,
            validators=[MinValueValidator(Decimal('0.01'))], default=Decimal(0))
    Date_inscription = models.DateField(default=timezone.now)
    Date_premium = models.DateField(default=timezone.now)
    date_atelier = models.DateField(default=timezone.now)
    Places = models.PositiveIntegerField(default=0)
    Messages = models.TextField()
    Commentaires = models.ManyToManyField(
        Commentaire,
        through='Ateliers_commentaires',
        through_fields=('ateliers', 'commentaires'),
    )
    picture = models.ImageField(upload_to='ateliers/%m/')
    def __str__(self): return self.Nom

class ateliers_themes(models.Model):
    ateliers = models.ForeignKey(Atelier, on_delete=models.CASCADE)
    themes = models.ForeignKey(Theme, on_delete=models.CASCADE)

class inscription_log(models.Model):
    atelier = models.ForeignKey(Atelier, on_delete=models.CASCADE)
    user = models.ForeignKey(
            'auth.User', on_delete=models.CASCADE,
            related_name='logs'
    )
    participants = models.ManyToManyField(
        Participant,
        through='participants_atelier',
        through_fields=('inscription_logs', 'participant')
    )
    Date = models.DateTimeField(default=timezone.now)

class participants_atelier(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    inscription_logs = models.ForeignKey(inscription_log, on_delete=models.CASCADE)

class ateliers_commentaires(models.Model):
    ateliers = models.ForeignKey(Atelier, on_delete=models.CASCADE)
    commentaires = models.ForeignKey(Commentaire, on_delete=models.CASCADE)

class ateliers_lieux(models.Model):
    ateliers = models.ForeignKey(Atelier, on_delete=models.CASCADE)
    lieux = models.ForeignKey(Lieu, on_delete=models.CASCADE)

class Chef(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    ateliers = models.ForeignKey(Atelier, on_delete=models.CASCADE)
