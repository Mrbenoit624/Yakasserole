from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

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

class Theme(models.Model):
    Name = models.CharField(max_length=65)

class Commentaire(models.Model):
    Titre = models.CharField(max_length=65)
    Messages = models.TextField()
    user_id = models.ForeignKey('auth.User', unique=True, on_delete=models.CASCADE)


class Recette(models.Model):
    Titre = models.CharField(max_length=65)
    Type_id = models.ForeignKey(Types, on_delete=models.CASCADE)
    Temps_preparation = models.DateTimeField()
    Temps_cuisson = models.DateTimeField()
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
    Nombre_portions = models.IntegerField(default=0)
    Difficulté = models.IntegerField(default=0)
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
    Date = models.DateTimeField()
    user_id = models.ForeignKey('auth.User', unique=True, on_delete=models.CASCADE)

class Lieu(models.Model):
    Nom = models.CharField(max_length=65)
    Adresse = models.CharField(max_length=65)
    Telephone = models.CharField(max_length=65)
    CodePostal = models.IntegerField(default=0)
    Ville = models.CharField(max_length=65)

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
    Chef_id = models.ForeignKey('auth.User', unique=True, on_delete=models.CASCADE)
    Date_inscription = models.DateTimeField()
    Date_premium = models.DateTimeField()
    Messages = models.TextField()
    Commentaires = models.ManyToManyField(
        Commentaire,
        through='Ateliers_commentaires',
        through_fields=('ateliers', 'commentaires'),
    )

#class inscription_log(models.Model):
#    user_id = models.ForeignKey('auth.User', unique=True, on_delete=models.CASCADE)
#    participants = models.ManyToManyField(
#        'auth.User',
#        through='paricipant_atelier',
#        through_fields=('users', 'inscription_logs'),
#    )
#    Date = models.DateTimeField()


#class paricipant_atelier(models.Model):
#    users = models.ForeignKey('auth.User', on_delete=models.CASCADE)
#    inscription_logs = models.ForeignKey(inscription_log, on_delete=models.CASCADE)

#class Chef(models.Model):
#    user_id = models.ForeignKey('auth.User', unique=True, on_delete=models.CASCADE)
#    ateliers = models.ManyToManyField(
#        Atelier,
#        through='Ateliers_chefs',
#        through_fields=('ateliers', 'chefs'),
#    )
#
#
#
#class ateliers_chefs(models.Model):
#    ateliers = models.ForeignKey(Atelier, on_delete=models.CASCADE)
#    chefs = models.ForeignKey(Chef, on_delete=models.CASCADE)

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

class ateliers_lieux(models.Model):
    ateliers = models.ForeignKey(Atelier, on_delete=models.CASCADE)
    lieux = models.ForeignKey(Lieu, on_delete=models.CASCADE)

class ateliers_themes(models.Model):
    ateliers = models.ForeignKey(Atelier, on_delete=models.CASCADE)
    themes = models.ForeignKey(Theme, on_delete=models.CASCADE)

class ateliers_commentaires(models.Model):
    ateliers = models.ForeignKey(Atelier, on_delete=models.CASCADE)
    commentaires = models.ForeignKey(Commentaire, on_delete=models.CASCADE)

