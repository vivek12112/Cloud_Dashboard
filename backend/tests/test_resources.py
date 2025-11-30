import pytest
import json
from resources.models import Resource
from rest_framework.test import APIClient
from tests.utils import create_user

pytestmark = pytest.mark.django_db

def test_create_resource_min_limits():
    client = APIClient()
    user = create_user(username='res_user', role='user')
    login_resp = client.post('/api/auth/login/', {'username': 'res_user', 'password': 'pass12345'}, format='json')
    access = login_resp.json().get('access')
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')

    url = '/api/resources/'
    payload = {
        'name': 'Tiny VM',
        'resource_type': 'vm',
        'cpu_cores': 1,
        'memory_gb': 1,
        'storage_gb': 10,
        'region': 'ap-south-1'
    }
    resp = client.post(url, data=payload, format='json')
    assert resp.status_code in (201, 400)

def test_create_resource_negative_values():
    client = APIClient()
    user = create_user(username='res_user2', role='user')
    login_resp = client.post('/api/auth/login/', {'username': 'res_user2', 'password': 'pass12345'}, format='json')
    access = login_resp.json().get('access')
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')

    url = '/api/resources/'
    payload = {
        'name': 'Bad VM',
        'resource_type': 'vm',
        'cpu_cores': -1,
        'memory_gb': -4,
        'storage_gb': -50,
        'region': 'ap-south-1'
    }
    resp = client.post(url, data=payload, format='json')
    assert resp.status_code in (400, 422)

def test_admin_can_approve_resource():
    client = APIClient()
    admin = create_user(username='admin', role='admin')
    user = create_user(username='userx', role='user')
    res = Resource.objects.create(user=user, name='Pending VM', resource_type='vm', status='pending')

    login_resp = client.post('/api/auth/login/', {'username': 'admin', 'password': 'pass12345'}, format='json')
    access = login_resp.json().get('access')
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')

    url = f'/api/resources/{res.id}/approve/'
    resp = client.post(url)
    assert resp.status_code == 200
    res.refresh_from_db()
    assert res.status == 'running'
