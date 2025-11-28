import pytest
from django.urls import reverse
from app_bibliothecaire.models import Emprunteur
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_removeemprunteur(client):
    user = User.objects.create_user("test_user", "testuser@gmail.com", "userpassword")
    client.login(username='test_user', password='userpassword')

    emprunteur = Emprunteur.objects.create(name='testemprunteur', firstname='testemprunteurnom', email='testemprunteur@gmail.com')

    response = client.post(reverse('delete_emprunteur', args=[emprunteur.id]))

    assert response.status_code == 302
    assert not Emprunteur.objects.filter(id=emprunteur.id).exists()