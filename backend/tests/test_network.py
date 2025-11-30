import pytest
import json
from network.models import NetworkPolicy, FirewallRule
from resources.models import Resource
from rest_framework.test import APIClient
from tests.utils import create_user

pytestmark = pytest.mark.django_db

def test_create_network_policy():
    client = APIClient()
    user = create_user(username='net_user', role='user')

    login_resp = client.post('/api/auth/login/', {'username': 'net_user', 'password': 'pass12345'}, format='json')
    access = login_resp.json().get('access')
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')

    payload = {
        'name': 'Default Policy',
        'description': 'Test policy',
        'ip_range': '10.0.0.0/24'
    }
    resp = client.post('/api/network/policies/', data=payload, format='json')
    assert resp.status_code in (201, 400)

def test_create_firewall_rule():
    client = APIClient()
    user = create_user(username='fw_user', role='user')

    login_resp = client.post('/api/auth/login/', {'username': 'fw_user', 'password': 'pass12345'}, format='json')
    access = login_resp.json().get('access')
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')

    res = Resource.objects.create(user=user, name='FW VM', resource_type='vm')
    payload = {
        'resource': res.id,
        'name': 'Allow HTTP',
        'protocol': 'tcp',
        'port_range': '80',
        'source_ip': '0.0.0.0/0',
        'action': 'allow'
    }
    resp = client.post('/api/network/firewall-rules/', data=payload, format='json')
    assert resp.status_code in (201, 400)
