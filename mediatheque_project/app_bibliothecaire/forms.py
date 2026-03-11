from django import forms
from .models import Emprunteur

choixMedia = [
    ('livre', 'Livre'),
    ('dvd', 'DVD'),
    ('cd', 'CD'),
    ('jeu', 'Jeu de Plateau'),
]

class CreationMediaForm(forms.Form):
    nom = forms.CharField(label="Nom", required=True)
    createur = forms.CharField(label="Auteur / Créateur", required=True)
    typeMedia = forms.ChoiceField(choices=choixMedia, label="Type de média")

class CreationEmprunteurForm(forms.ModelForm):
    class Meta:
        model = Emprunteur
        fields = ['nom', 'prenom', 'email']

class BorrowMediaForm(forms.Form):
    emprunteur = forms.ModelChoiceField(
        queryset=Emprunteur.objects.all(),
        label="emprunteur",
        widget=forms.Select(attrs={"class": "searchable"})
    )

    typeMedia = forms.ChoiceField(
        choices=choixMedia,
        label="Type de média",
        widget=forms.Select(attrs={"id": "typeMedia"})
    )

    idMedia = forms.IntegerField(widget=forms.HiddenInput())