import os
import json

import pytest

os.environ['DATABASE'] = 'users_test.db'

from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client


@pytest.fixture
def user(client):
    data = {
        'name': 'User',
        'last_name': 'Test',
        'email': 'TEST@test.com',
        'date': 'none',
        'password': 'test-test'
    }
    response = client.post('/users', data=json.dumps(data))
    user = json.loads(response.data)
    user.update(data)
    print(user)

    yield user

    client.delete('/users/{}'.format(user['id']))


def test_users_get(client, user):
    response = client.get('/users')
    data = json.loads(response.data)
    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0].get('id') == user['id']
