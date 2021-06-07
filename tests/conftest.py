import json

import pytest

from app import app

@pytest.fixture(scope='module')
def client():
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client


@pytest.fixture(scope='module')
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

    yield user

    client.delete('/users/{}'.format(user['id']))


@pytest.fixture(scope='module')
def prescription(client, user):
    prescription = {
        'user_id': user['id'],
        'prescription_date': '00-00-2000',
        'od': 'GRADUACION OD',
        'oi': 'GRADUACION OI',
        'addition': '5.00',
        'notes': 'ametropia',
        'doctor': 'EZEQUIEL ROMIO'
    }

    response = client.post('/prescriptions', data=json.dumps(prescription))
    prescription['id'] = json.loads(response.data)['id']

    yield prescription

    client.delete('/prescriptions/{}'.format(prescription['id']))


