from django import forms

class Creationlivre(forms.Form):
    nom = forms.CharField(required=False)
    auteur = forms.CharField(required=False)

class CreationDvd(forms.Form):
    nom = forms.CharField(required=False)
    auteur = forms.CharField(required=False)

class CreationCd(forms.Form):
    nom = forms.CharField(required=False)
    auteur = forms.CharField(required=False)

class CreationJeuDePlateau(forms.Form):
    nom = forms.CharField(required=False)
    auteur = forms.CharField(required=False)