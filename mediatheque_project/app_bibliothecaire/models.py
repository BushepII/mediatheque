from django.db import models
from django.utils import timezone
from datetime import timedelta

class Medias(models.Model):
    name = models.fields.CharField(max_length=150)
    dateEmprunt = models.DateTimeField(blank=True, null=True)
    dateRetour = models.DateTimeField(blank=True, null=True)
    disponible = models.BooleanField(default=True)
    emprunteur = models.CharField(max_length=150)

    class Meta:
        abstract = True

    def mark_borrowed(self, borrower_name, days=7):
        self.disponible = False
        self.emprunteur = borrower_name
        self.dateEmprunt = timezone.now()
        self.dateRetour = timezone.now() + timedelta(days=days)
        self.save()

    def mark_returned(self):
        self.disponible = True
        self.emprunteur = ""
        self.dateEmprunt = None
        self.dateRetour = None
        self.save()

    def is_overdue(self):
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
    name = models.fields.CharField(max_length=150)
    createur = models.CharField(max_length=150)
    disponible = models.BooleanField(default=False)

class Emprunteur(models.Model):
    name = models.fields.CharField(max_length=150)
    firstname = models.fields.CharField(max_length=150)
    email = models.EmailField(unique=True, blank=False, null=False)
    bloque = models.BooleanField(default=False)

    def __str__(self):
        return self.name

def default_date_retour():
    return timezone.now() + timedelta(days=7)

class Emprunt(models.Model):
    MEDIA_CHOICES = [
        ('livre', 'Livre'),
        ('dvd', 'DVD'),
        ('cd', 'CD'),
        ('jeu', 'Jeu de Plateau'),
    ]

    borrower = models.ForeignKey(Emprunteur, on_delete=models.PROTECT)
    media_type = models.CharField(max_length=10, choices=MEDIA_CHOICES)
    media_id = models.IntegerField()  # stores the id of the specific media
    date_emprunt = models.DateTimeField(default=timezone.now)
    date_retour = models.DateTimeField(default=default_date_retour)
    returned = models.BooleanField(default=False)

    def is_overdue(self):
        return not self.returned and timezone.now() > self.date_retour

    def __str__(self):
        return f"{self.borrower.name} - {self.media_type} ({self.media_id})"