import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework.reverse import reverse as drf_reverse

User = get_user_model()

pytestmark = pytest.mark.django_db

def test_register_user_edge_password_mismatch():
    client = APIClient()
    url = '/api/auth/register/'
    payload = {
        'username': 'edge_user',
        'email': 'edge@example.com',
        'password': 'pass12345',
        'password2': 'pass99999',
        'role': 'user'
    }
    resp = client.post(url, data=payload, format='json')
    assert resp.status_code == 400

def test_login_and_me_endpoint():
    client = APIClient()
    User.objects.create_user(username='john', password='pass12345', role='user', email='john@example.com')

    login_url = '/api/auth/login/'
    resp = client.post(login_url, {'username': 'john', 'password': 'pass12345'}, format='json')
    assert resp.status_code == 200
    tokens = resp.json()
    assert 'access' in tokens
    access = tokens['access']

    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
    me_url = '/api/auth/me/'
    resp2 = client.get(me_url)
    assert resp2.status_code == 200
    me = resp2.json()
    assert me['username'] == 'john'
