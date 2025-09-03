from django import forms

class Creationlivre(forms.Form):
    nom = forms.CharField(required=False)
    auteur = forms.CharField(required=False)