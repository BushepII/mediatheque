import pytest
from django.urls import reverse
from app_bibliothecaire.models import Emprunt, Emprunteur, Livre
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

from app_bibliothecaire.views import peutEmprunter


@pytest.mark.django_db
def test_emprunt(client):
    user = User.objects.create_user("test_user", "testuser@gmail.com", "userpassword")
    client.login(username='test_user', password='userpassword')

    emprunteur1 = Emprunteur.objects.create(nom='testemprunteur', prenom='testemprunteurnom',
                                           email='testemprunteur@gmail.com')

    emprunteur2 = Emprunteur.objects.create(nom='testemprunteur2', prenom='testemprunteurnom2',
                                            email='testemprunteur2@gmail.com')

    emprunteur3 = Emprunteur.objects.create(nom='testemprunteur3', prenom='testemprunteurnom3',
                                            email='testemprunteur3@gmail.com')

    livre1 = Livre.objects.create(nom="livre1", auteur="a1", disponible=True)
    livre2 = Livre.objects.create(nom="livre2", auteur="a2", disponible=True)
    livre3 = Livre.objects.create(nom="livre3", auteur="a3", disponible=True)
    livre4 = Livre.objects.create(nom="livre4", auteur="a4", disponible=True)
    livre5 = Livre.objects.create(nom="livre5", auteur="a5", disponible=True)

    url = reverse("pageEmprunt")

    def emprunt(livre, emprunteur):
        return client.post(url, {
            'emprunteur': emprunteur.id,
            'typeMedia': 'livre',
            'idMedia': livre.id,
        })

    emprunt(livre1, emprunteur1)
    emprunt(livre2, emprunteur1)
    emprunt(livre3, emprunteur1)

    reponseMultiplesEmprunts = emprunt(livre4, emprunteur1)

    assert reponseMultiplesEmprunts.status_code == 302

    assert Emprunt.objects.filter(emprunteur=emprunteur1, mediaRendu=False).count() == 3

    livre3.refresh_from_db()
    livre4.refresh_from_db()
    emprunteur1.refresh_from_db()
    assert livre3.disponible is False
    assert livre4.disponible is True
    assert emprunteur1.bloque is True

    emprunt(livre5, emprunteur2)

    emprunt = Emprunt.objects.get(
        emprunteur=emprunteur2,
        typeMedia="livre",
        idMedia=livre5.id,
        mediaRendu=False,
    )

    emprunt.dateEmprunt = timezone.now() - timedelta(days=60)
    emprunt.dateRetour = timezone.now() - timedelta(days=30)
    emprunt.save()

    emprunt.refresh_from_db()
    assert Emprunt.objects.filter(emprunteur=emprunteur2, mediaRendu=False).count() == 1
    assert emprunt.dateRetour < timezone.now()
    assert peutEmprunter(emprunteur2) is False
    emprunteur2.refresh_from_db()
    assert emprunteur2.bloque is True


    assert Emprunt.objects.filter(emprunteur=emprunteur3, mediaRendu=False).count() == 0
