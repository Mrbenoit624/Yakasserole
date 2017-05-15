from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator
from community.models import Commentaire
import datetime
from decimal import Decimal

class Type(models.Model):
    Name = models.CharField(max_length=65)
    def __str__(self): return self.Name

class Ustensile(models.Model):
    Name = models.CharField(max_length=65)
    def __str__(self): return self.Name

class Electromenager(models.Model):
    Name = models.CharField(max_length=65)
    def __str__(self): return self.Name

class Ingredient(models.Model):
    Name = models.CharField(max_length=65)
    def __str__(self): return self.Name

class Etape(models.Model):
    Titre = models.CharField(max_length=65)
    Contenu = models.TextField(default='')

class Recette(models.Model):
    Titre = models.CharField(max_length=65)
    Type = models.ForeignKey(Type, on_delete=models.CASCADE)
    Temps_preparation = models.TimeField()
    Temps_cuisson = models.TimeField()
    Ustensiles = models.ManyToManyField(
        Ustensile,
        through='Recettes_Ustensiles',
        through_fields=('recettes', 'ustensiles'),
    )
    Electromenager = models.ManyToManyField(
        Electromenager,
        through='Recettes_Electromenager',
        through_fields=('recettes', 'electromenagers'),
    )
    Nombre_portions = models.PositiveIntegerField(default=0)
    Difficulte = models.PositiveIntegerField(default=0)
    Cout = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], default=Decimal(1.00))
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
    Remarques = models.TextField()
    Commentaires = models.ManyToManyField(
        Commentaire,
        through='Recettes_Commentaires',
        through_fields=('recettes', 'commentaires'),
    )
    Date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)


class recettes_ustensiles(models.Model):
    recettes = models.ForeignKey(Recette, on_delete=models.CASCADE)
    ustensiles = models.ForeignKey(Ustensile, on_delete=models.CASCADE)

class recettes_electromenager(models.Model):
    recettes = models.ForeignKey(Recette, on_delete=models.CASCADE)
    electromenagers = models.ForeignKey(Electromenager, on_delete=models.CASCADE)

class recettes_ingredients(models.Model):
    recettes = models.ForeignKey(Recette, on_delete=models.CASCADE)
    ingredients = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

class recettes_etapes(models.Model):
    recettes = models.ForeignKey(Recette, on_delete=models.CASCADE)
    etapes = models.ForeignKey(Etape, on_delete=models.CASCADE)

class recettes_commentaires(models.Model):
    recettes = models.ForeignKey(Recette, on_delete=models.CASCADE)
    commentaires = models.ForeignKey(Commentaire, on_delete=models.CASCADE)
