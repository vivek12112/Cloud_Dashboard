import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from tests.utils import create_user

pytestmark = pytest.mark.django_db

def test_admin_can_list_users():
    client = APIClient()
    admin = create_user(username='admin_u', role='admin')
    create_user(username='user1_u', role='user')

    login_resp = client.post('/api/auth/login/', {'username': 'admin_u', 'password': 'pass12345'}, format='json')
    access = login_resp.json().get('access')
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')

    url = reverse('list_users')
    resp = client.get(url)
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) >= 2

def test_non_admin_cannot_list_users():
    client = APIClient()
    user = create_user(username='normal_u', role='user')

    login_resp = client.post('/api/auth/login/', {'username': 'normal_u', 'password': 'pass12345'}, format='json')
    access = login_resp.json().get('access')
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')

    url = reverse('list_users')
    resp = client.get(url)
    assert resp.status_code == 403
