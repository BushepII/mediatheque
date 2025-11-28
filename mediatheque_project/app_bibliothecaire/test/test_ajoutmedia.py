import pytest
from django.urls import reverse
from app_bibliothecaire.models import Livre
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_ajoutmedia(client):
    user = User.objects.create_user("test_user", "testuser@gmail.com", "userpassword")
    client.login(username='test_user', password='userpassword')

    data = {
        'nom' : 'testlivre',
        'createur': 'testauteurlivre',
        'media_type':'livre'
    }

    response = client.post(reverse('ajoutmedia'), data)

    assert response.status_code == 302
    assert response.url == reverse('ajoutmedia')

    assert Livre.objects.filter(name='testlivre', auteur='testauteurlivre').exists()