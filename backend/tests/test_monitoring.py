import pytest
from monitoring.models import Metric, Alert
from resources.models import Resource
from rest_framework.test import APIClient
from tests.utils import create_user

pytestmark = pytest.mark.django_db

def test_dashboard_stats_shape():
    client = APIClient()
    admin = create_user(username='admin_m', role='admin')
    user = create_user(username='user_m', role='user')
    Resource.objects.create(user=user, name='R1', resource_type='vm', status='running')
    Alert.objects.create(user=user, message='High CPU', severity='warning', is_resolved=False)

    login_resp = client.post('/api/auth/login/', {'username': 'admin_m', 'password': 'pass12345'}, format='json')
    access = login_resp.json().get('access')
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')

    resp = client.get('/api/monitoring/dashboard-stats/')
    assert resp.status_code == 200
    data = resp.json()
    for key in ['total_resources', 'active_resources', 'pending_resources', 'total_users', 'unresolved_alerts']:
        assert key in data

def test_generate_mock_metrics_multiple_calls():
    client = APIClient()
    user = create_user(username='user_mm', role='user')

    login_resp = client.post('/api/auth/login/', {'username': 'user_mm', 'password': 'pass12345'}, format='json')
    access = login_resp.json().get('access')
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')

    res = Resource.objects.create(user=user, name='Mon VM', resource_type='vm', status='running')
    for _ in range(5):
        resp = client.post('/api/monitoring/generate-metrics/', {'resource_id': res.id}, format='json')
        assert resp.status_code == 201
    assert Metric.objects.filter(resource=res).count() >= 5
