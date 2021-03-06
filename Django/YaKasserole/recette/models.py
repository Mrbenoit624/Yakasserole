from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
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

def validate_file_extension(val):
    if not val.name.endswith('.mp4'):
        raise ValidationError(u'La vidéo doit être au format mp4')

class Recette(models.Model):
    Titre = models.CharField(max_length=65)
    Type = models.ForeignKey(Type, on_delete=models.CASCADE, default="")
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
    Nombre_portions = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    Difficulte = models.IntegerField(validators=[MaxValueValidator(5)],
            choices=[(i+1,i+1) for i in range(5)])
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
    video = models.FileField(upload_to='recettes/%m/%d/', blank=True, null=False, validators=[validate_file_extension])

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
