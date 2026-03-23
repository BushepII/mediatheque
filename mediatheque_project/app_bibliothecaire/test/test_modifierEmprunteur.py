import pytest
from django.urls import reverse
from app_bibliothecaire.models import Emprunteur
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_modifierEmprunteur(client):
    user = User.objects.create_user("test_user", "testuser@gmail.com", "userpassword")
    client.login(username='test_user', password='userpassword')

    emprunteur = Emprunteur.objects.create(nom='testemprunteur', prenom='testemprunteurnom', email='testemprunteur@gmail.com')

    response = client.post(reverse('modifierEmprunteur', args=[emprunteur.id]), {'nom':'testnom2', 'prenom':'testprenom2',
                                                                                        'email':'testuser2@gmail.com'})

    assert response.status_code == 200

    emprunteur.refresh_from_db()
    assert emprunteur.nom == 'testnom2'
    assert emprunteur.prenom == 'testprenom2'
    assert emprunteur.email == 'testuser2@gmail.com'