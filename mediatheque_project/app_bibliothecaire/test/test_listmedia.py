import pytest
from django.urls import reverse
from app_bibliothecaire.models import Livre, Dvd, Cd, JeuDePlateau
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_listemedia(client):
    Livre.objects.create(name='testlivre', auteur='auteurtest')
    Dvd.objects.create(name='testdvd', realisateur='realisateurtest')
    Cd.objects.create(name='testcd', artiste='artistetest')
    JeuDePlateau.objects.create(name='testjeudeplateau', createur='createurtest')

    response = client.post(reverse('home'))
    assert 'testlivre' in response.content.decode()
    assert 'testdvd' in response.content.decode()
    assert 'testcd' in response.content.decode()
    assert 'testjeudeplateau' in response.content.decode()