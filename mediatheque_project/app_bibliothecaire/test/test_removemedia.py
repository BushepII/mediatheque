import pytest
from django.urls import reverse
from app_bibliothecaire.models import Livre
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_removemedia(client):
    user = User.objects.create_user("test_user", "testuser@gmail.com", "userpassword")
    client.login(username='test_user', password='userpassword')

    livre = Livre.objects.create(name='testlivre', auteur='auteurtest')

    response = client.post(reverse('delete_media', args=['livre', livre.id]))

    assert response.status_code == 302
    assert not Livre.objects.filter(id=livre.id).exists()