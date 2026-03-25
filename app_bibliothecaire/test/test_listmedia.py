import pytest
from django.urls import reverse
from app_bibliothecaire.models import Livre, Dvd, Cd, JeuDePlateau

@pytest.mark.django_db
def test_listemedia(client):
    Livre.objects.create(nom='testlivre', auteur='auteurtest')
    Dvd.objects.create(nom='testdvd', realisateur='realisateurtest')
    Cd.objects.create(nom='testcd', artiste='artistetest')
    JeuDePlateau.objects.create(nom='testjeudeplateau', createur='createurtest')

    response = client.post(reverse('home'))
    assert 'testlivre' in response.content.decode()
    assert 'testdvd' in response.content.decode()
    assert 'testcd' in response.content.decode()
    assert 'testjeudeplateau' in response.content.decode()