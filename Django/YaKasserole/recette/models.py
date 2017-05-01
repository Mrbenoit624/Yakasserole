from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from community.models import Commentaire
import datetime

class Types(models.Model):
    Name = models.CharField(max_length=65)

class Ustensile(models.Model):
    Name = models.CharField(max_length=65)

class Electromenager(models.Model):
    Name = models.CharField(max_length=65)

class Ingredient(models.Model):
    Name = models.CharField(max_length=65)

class Etape(models.Model):
    Name = models.CharField(max_length=65)

class Recette(models.Model):
    Titre = models.CharField(max_length=65)
    Type_id = models.ForeignKey(Types, on_delete=models.CASCADE)
    Temps_preparation = models.DateTimeField(default=timezone.now)
    Temps_cuisson = models.DateTimeField(default=timezone.now)
    Ustensiles = models.ManyToManyField(
        Ustensile,
        through='Recettes_Ustensiles',
        through_fields=('recettes', 'ustensiles'),
    )
    Electromenager = models.ManyToManyField(
        Electromenager,
        through='Recettes_Electromenager',
        through_fields=('recettes', 'elctromenagers'),
    )
    Nombre_portions = models.PositiveIntegerField(default=0)
    Difficulte = models.PositiveIntegerField(default=0)
    Cout = models.FloatField(default=0)
    Ingredients = models.ManyToManyField(
        Ingredient,
        through='Recettes_Ingredients',
        through_fields=('recettes', 'ingredients'),
    )
    Etapes = models.ManyToManyField(
        Etape,
        through='Recettes_Etapes',
        through_fields=('recettes', 'etapes'),
    )
    Remarques = models.CharField(max_length=255)
    Commentaires = models.ManyToManyField(
        Commentaire,
        through='Recettes_Commentaires',
        through_fields=('recettes', 'commentaires'),
    )
    Date = models.DateTimeField(default=timezone.now)
    user_id = models.ForeignKey('auth.User', on_delete=models.CASCADE)


class recettes_ustensiles(models.Model):
    recettes = models.ForeignKey(Recette, on_delete=models.CASCADE)
    ustensiles = models.ForeignKey(Ustensile, on_delete=models.CASCADE)

class recettes_electromenager(models.Model):
    recettes = models.ForeignKey(Recette, on_delete=models.CASCADE)
    elctromenagers = models.ForeignKey(Electromenager, on_delete=models.CASCADE)

class recettes_ingredients(models.Model):
    recettes = models.ForeignKey(Recette, on_delete=models.CASCADE)
    ingredients = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

class recettes_etapes(models.Model):
    recettes = models.ForeignKey(Recette, on_delete=models.CASCADE)
    etapes = models.ForeignKey(Etape, on_delete=models.CASCADE)

class recettes_commentaires(models.Model):
    recettes = models.ForeignKey(Recette, on_delete=models.CASCADE)
    commentaires = models.ForeignKey(Commentaire, on_delete=models.CASCADE)
