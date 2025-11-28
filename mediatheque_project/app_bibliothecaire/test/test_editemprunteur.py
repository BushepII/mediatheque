import pytest
from django.urls import reverse
from app_bibliothecaire.models import Emprunteur
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_editemprunteur(client):
    user = User.objects.create_user("test_user", "testuser@gmail.com", "userpassword")
    client.login(username='test_user', password='userpassword')

    emprunteur = Emprunteur.objects.create(name='testemprunteur', firstname='testemprunteurnom', email='testemprunteur@gmail.com')

    response = client.post(reverse('edit_emprunteur', args=[emprunteur.id]), {'name':'testname2', 'firstname':'testprenom2',
                                                                                        'email':'testuser2@gmail.com'})

    assert response.status_code == 302

    emprunteur.refresh_from_db()
    assert emprunteur.name == 'testname2'
    assert emprunteur.firstname == 'testprenom2'
    assert emprunteur.email == 'testuser2@gmail.com'