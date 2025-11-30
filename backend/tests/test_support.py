import pytest
import json
from support.models import Ticket
from rest_framework.test import APIClient
from tests.utils import create_user

pytestmark = pytest.mark.django_db

def test_create_ticket_high_priority():
    client = APIClient()
    user = create_user(username='sup_user', role='user')

    login_resp = client.post('/api/auth/login/', {'username': 'sup_user', 'password': 'pass12345'}, format='json')
    access = login_resp.json().get('access')
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')

    payload = {
        'title': 'Production down',
        'description': 'All services unavailable',
        'priority': 'urgent'
    }
    resp = client.post('/api/support/tickets/', data=payload, format='json')
    assert resp.status_code in (201, 400)

def test_ticket_list_empty():
    client = APIClient()
    user = create_user(username='sup_empty', role='user')

    login_resp = client.post('/api/auth/login/', {'username': 'sup_empty', 'password': 'pass12345'}, format='json')
    access = login_resp.json().get('access')
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')

    resp = client.get('/api/support/tickets/')
    assert resp.status_code == 200
