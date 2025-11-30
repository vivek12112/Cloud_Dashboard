import pytest
from datetime import datetime
from decimal import Decimal
from billing.models import BillingRecord
from resources.models import Resource
from rest_framework.test import APIClient
from tests.utils import create_user

pytestmark = pytest.mark.django_db

def test_billing_summary_user_limits():
    client = APIClient()
    user = create_user(username='bill_user', role='user')

    login_resp = client.post('/api/auth/login/', {'username': 'bill_user', 'password': 'pass12345'}, format='json')
    access = login_resp.json().get('access')
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')

    res = Resource.objects.create(user=user, name='Bill VM', resource_type='vm', status='running', cost_per_hour=Decimal('0.1'))
    BillingRecord.objects.create(
        user=user,
        resource=res,
        usage_hours=Decimal('0.00'),
        cost_per_hour=Decimal('0.1'),
        total_cost=Decimal('0.00'),
        billing_date=datetime.now().date()
    )

    resp = client.get('/api/billing/summary/')
    assert resp.status_code == 200
    data = resp.json()
    assert 'total_cost' in data

def test_billing_records_empty():
    client = APIClient()
    user = create_user(username='bill_empty', role='user')

    login_resp = client.post('/api/auth/login/', {'username': 'bill_empty', 'password': 'pass12345'}, format='json')
    access = login_resp.json().get('access')
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')

    resp = client.get('/api/billing/records/')
    assert resp.status_code == 200
