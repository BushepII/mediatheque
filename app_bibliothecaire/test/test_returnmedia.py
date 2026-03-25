import pytest
from django.urls import reverse
from app_bibliothecaire.models import Emprunt, Emprunteur, Livre
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_ajoutmedia(client):
    user = User.objects.create_user("test_user", "testuser@gmail.com", "userpassword")
    client.login(username='test_user', password='userpassword')

    emprunteur1 = Emprunteur.objects.create(nom='testemprunteur', prenom='testemprunteurnom',
                                           email='testemprunteur@gmail.com')

    livre1 = Livre.objects.create(nom="livre1", auteur="a1", disponible=True)

    url = reverse("pageEmprunt")

    def emprunt(livre, emprunteur):
        return client.post(url, {
            'emprunteur': emprunteur.id,
            'typeMedia': 'livre',
            'idMedia': livre.id,
        })

    emprunt(livre1, emprunteur1)

    livre1.refresh_from_db()
    emprunteur1.refresh_from_db()

    response =  client.post(reverse('retourMedia', args=['livre', livre1.id]))

    livre1.refresh_from_db()
    emprunteur1.refresh_from_db()

    assert response.status_code == 302
    assert livre1.disponible is True
    assert Emprunt.objects.filter(emprunteur=emprunteur1, mediaRendu=False).count() == 0
