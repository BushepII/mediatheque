import pytest
from django.urls import reverse
from app_bibliothecaire.models import Emprunteur
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_ajoutemprunteur(client):
    user = User.objects.create_user("test_user", "testuser@gmail.com", "userpassword")
    client.login(username='test_user', password='userpassword')

    data = {
        'nom' : 'testemprunteur',
        'prenom': 'testprenomemprunteur',
        'email': 'testemprunteur@gmail.com'
    }

    response = client.post(reverse('ajoutEmprunteur'), data)

    assert response.status_code == 302
    assert response.url == reverse('ajoutEmprunteur')

    assert Emprunteur.objects.filter(nom='testemprunteur', prenom='testprenomemprunteur', email='testemprunteur@gmail.com').exists()