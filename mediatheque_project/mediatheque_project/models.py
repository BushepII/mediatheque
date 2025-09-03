from django.db import models
from django.utils import timezone

class Medias(models.Model):
    name = models.fields.CharField(max_length=150)
    dateEmprunt = models.DateTimeField(default=timezone.now)
    disponible = models.BooleanField(default=True)
    emprunteur = models.CharField(max_length=150)

    class Meta:
        abstract = True

class Livre(Medias):
    auteur = models.CharField(max_length=150)

class Dvd(Medias):
    realisateur = models.CharField(max_length=150)

class Cd(Medias):
    artiste = models.CharField(max_length=150)

class JeuDePlateau(models.Model):
    name = models.fields.CharField(max_length=150)
    createur = models.CharField(max_length=150)

class Emprunteur(models.Model):
    name = models.fields.CharField(max_length=150)
    bloque = models.BooleanField(default=False)