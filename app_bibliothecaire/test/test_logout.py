import pytest
from django.urls import reverse
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_logout(client):
    user = User.objects.create_user("test_user", "testuser@gmail.com", "userpassword")
    client.login(username='test_user', password='userpassword')

    response = client.post(reverse('logout'))

    assert response.status_code == 302
    assert response.url == reverse('home')