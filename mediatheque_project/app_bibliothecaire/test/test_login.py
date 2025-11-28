import pytest
from django.urls import reverse
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_login(client):
    user = User.objects.create_user("test_user", "testuser@gmail.com", "userpassword")

    response = client.post(reverse('login'), {'username': 'test_user', 'password': 'userpassword'})
    assert response.status_code == 302
    assert response.url != reverse('login')

    #Test with wrong user
    response = client.post(reverse('login'), {'username': 'test_user', 'password': 'wrongpassword'})
    assert response.status_code == 302
    assert response.url == reverse('login')