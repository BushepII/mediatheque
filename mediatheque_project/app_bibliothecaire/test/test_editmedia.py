import pytest
from django.urls import reverse
from app_bibliothecaire.models import Livre
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_editmedia(client):
    user = User.objects.create_user("test_user", "testuser@gmail.com", "userpassword")
    client.login(username='test_user', password='userpassword')

    livre = Livre.objects.create(name='testlivre', auteur='auteurtest')

    data = {
        'nom': 'testlivre2',
        'createur': 'testauteurlivre2',
        'media_type': 'livre'
    }

    response = client.post(reverse('edit_media', args=['livre', livre.id]), data)

    assert response.status_code == 302

    livre.refresh_from_db()
    assert livre.name == 'testlivre2'
    assert livre.auteur == 'testauteurlivre2'