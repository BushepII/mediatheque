import pytest
from django.urls import reverse
from app_bibliothecaire.models import Emprunt, Emprunteur, JeuDePlateau
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

from app_bibliothecaire.views import peutEmprunter


@pytest.mark.django_db
def test_ajoutmedia(client):
    user = User.objects.create_user("test_user", "testuser@gmail.com", "userpassword")
    client.login(username='test_user', password='userpassword')

    emprunteur1 = Emprunteur.objects.create(nom='testemprunteur', prenom='testemprunteurnom',
                                           email='testemprunteur@gmail.com')

    jeu1 = JeuDePlateau.objects.create(nom="jeu1", createur="j1", disponible=True)

    url = reverse("pageEmprunt")

    def emprunt(jeu, emprunteur):
        return client.post(url, {
            'emprunteur': emprunteur.id,
            'typeMedia': 'jeu',
            'idMedia': jeu.id,
        })

    response = emprunt(jeu1, emprunteur1)
    assert response.status_code == 302
    jeu1.refresh_from_db()
    emprunteur1.refresh_from_db()
    assert Emprunt.objects.filter(emprunteur=emprunteur1, mediaRendu=False).count() == 0
    assert jeu1.disponible is True

