from django import forms
from .models import Emprunteur

MEDIA_CHOICES = [
    ('livre', 'Livre'),
    ('dvd', 'DVD'),
    ('cd', 'CD'),
    ('jeu', 'Jeu de Plateau'),
]

class CreationMediaForm(forms.Form):
    nom = forms.CharField(label="Nom", required=True)
    createur = forms.CharField(label="Auteur / Créateur", required=True)
    media_type = forms.ChoiceField(choices=MEDIA_CHOICES, label="Type de média")

class CreationEmprunteurForm(forms.ModelForm):
    class Meta:
        model = Emprunteur
        fields = ['name', 'firstname', 'email']

class BorrowMediaForm(forms.Form):
    borrower = forms.ModelChoiceField(
        queryset=Emprunteur.objects.all(),
        label="Emprunteur",
        widget=forms.Select(attrs={"class": "searchable"})
    )

    media_type = forms.ChoiceField(
        choices=MEDIA_CHOICES,
        label="Type de média",
        widget=forms.Select(attrs={"id": "media_type"})
    )

    media_id = forms.IntegerField(widget=forms.HiddenInput())