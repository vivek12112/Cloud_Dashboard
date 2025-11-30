from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

def create_user(username='user1', password='pass12345', role='user', **extra):
    user = User.objects.create_user(
        username=username,
        password=password,
        role=role,
        email=extra.get('email', f'{username}@example.com'),
        first_name=extra.get('first_name', 'Test'),
        last_name=extra.get('last_name', 'User'),
    )
    return user

def auth_headers(client, username, password):
    from rest_framework.reverse import reverse as drf_reverse
    url = drf_reverse('token_obtain_pair')
    resp = client.post(url, {'username': username, 'password': password}, content_type='application/json')
    assert resp.status_code == 200
    access = resp.json()['access']
    return {'HTTP_AUTHORIZATION': f'Bearer {access}'}
