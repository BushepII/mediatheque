from django.db import models
from django.utils import timezone
from datetime import timedelta

class Medias(models.Model):
    nom = models.fields.CharField(max_length=150)
    dateEmprunt = models.DateTimeField(blank=True, null=True)
    dateRetour = models.DateTimeField(blank=True, null=True)
    disponible = models.BooleanField(default=True)
    emprunteur = models.CharField(max_length=150)

    class Meta:
        abstract = True

    def etatEmprunte(self, nomEmprunteur, days=7):
        self.disponible = False
        self.emprunteur = nomEmprunteur
        self.dateEmprunt = timezone.now()
        self.dateRetour = timezone.now() + timedelta(days=days)
        self.save()

    def etatRetourne(self):
        self.disponible = True
        self.emprunteur = ""
        self.dateEmprunt = None
        self.dateRetour = None
        self.save()

    def retard(self):
        if self.dateRetour and not self.disponible:
            return timezone.now() > self.dateRetour
        return False

class Livre(Medias):
    auteur = models.CharField(max_length=150)

class Dvd(Medias):
    realisateur = models.CharField(max_length=150)

class Cd(Medias):
    artiste = models.CharField(max_length=150)

class JeuDePlateau(models.Model):
    nom = models.fields.CharField(max_length=150)
    createur = models.CharField(max_length=150)
    disponible = models.BooleanField(default=False)

class Emprunteur(models.Model):
    nom = models.fields.CharField(max_length=150)
    prenom = models.fields.CharField(max_length=150)
    email = models.EmailField(unique=True, blank=False, null=False)
    bloque = models.BooleanField(default=False)

    def __str__(self):
        return self.nom

def dateRetourDefaut():
    return timezone.now() + timedelta(days=7)

class Emprunt(models.Model):
    choixMedia = [
        ('livre', 'Livre'),
        ('dvd', 'DVD'),
        ('cd', 'CD'),
    ]

    emprunteur = models.ForeignKey(Emprunteur, on_delete=models.PROTECT)
    typeMedia = models.CharField(max_length=10, choices=choixMedia)
    idMedia = models.IntegerField()
    dateEmprunt = models.DateTimeField(default=timezone.now)
    dateRetour = models.DateTimeField(default=dateRetourDefaut)
    mediaRendu = models.BooleanField(default=False)

    def is_overdue(self):
        return not self.mediaRendu and timezone.now() > self.dateRetour

    def __str__(self):
        return f"{self.emprunteur.nom} - {self.typeMedia} ({self.idMedia})"