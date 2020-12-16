import os
import json

import pytest

os.environ['DATABASE'] = 'users_test.db'

import create_data_base

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

    yield user

    client.delete('/users/{}'.format(user['id']))


###################### post tests ##########################

def test_users_post(client):
    data = {
        'name': 'pablo',
        'last_name': 'diaz_ogni',
        'email': 'pbldo@perro.com',
        'date': 'none',
        'password': 'ehehehehhe'
    }

    response = client.post('/users', data=json.dumps(data))
    user = json.loads(response.data)

    assert response.status_code == 200
    assert 'id' in user 
    client.delete('/users/{}'.format(user['id']))


def test_users_post_400_missing_field(client):
    #'name': 'pablo', FALTARÍA EL NOMBRE
    data = {
        'last_name': 'diaz_ogni',
        'email': 'pbldo@perro.com',
        'date': 'none',
        'password': 'ehehehehhe'
    }

    response = client.post('/users', data=json.dumps(data))
    print(json.loads(response.data))
    assert response.status_code == 400


################## get tests ##################

def test_users_get_ok(client, user):
    print(user)
    response = client.get('/users/{}'.format(user['id']), data=json.dumps([]))
    user_data = json.loads(response.data)
    
    assert 'date' in user_data
    assert isinstance(user_data, dict)
    assert response.status_code == 200
    
    print(user)


def test_users_get_selected_fields(client, user):
    response = client.get('/users/{}'.format(user['id']), data=json.dumps(['name', 'email']))
    
    user = json.loads(response.data)

    assert 'password' not in user
    assert 'name' in user
    assert response.status_code == 200
    
    print(user)


def test_password_hash(client, user):
    password = user['password']
    response = client.get('/users/{}'.format(user['id']), data=json.dumps(['password']))
    hashed = json.loads(response.data)

    assert password != hashed['password']
    assert response.status_code == 200
    

def test_users_get_404(client):
    response = client.get('/users/0', data=json.dumps([]))
    
    print(json.loads(response.data))
    assert response.status_code == 404


def test_users_get_list(client, user):
    response = client.get('/users')
    data = json.loads(response.data)
    print(data)
    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0].get('id') == user['id']


############### put tests ###############

def test_users_put_ok(client, user):
    data = {
        'name': 'Camila', 
        'last_name': 'Grosso', 
        'email': 'camilagros@etc.com', 
        'date': '2020-10-06 19:37:38',
        'password': 'k-1000-A'
    }

    response = client.put('/users/{}'.format(user['id']), data=json.dumps(data))

    assert response.status_code == 200

    user_updated = client.get('/users/{}'.format(user['id']), data=json.dumps([]))
    user_updated = json.loads(user_updated.data)
    user_updated['password'] = json.loads(client.get('/users/{}'.format(user['id']), data=json.dumps(['password'])).data)

    for key in data.keys():
        print(data[key], user_updated[key])
        if key == 'date':
            continue
        elif key == 'password':
            assert data[key] != user_updated[key]
        elif key != 'id':
            print(data[key], user_updated[key])
            assert data[key] == user_updated[key]
    
    for key in user_updated.keys():
        if key not in data:
            assert user_updated[key] == user[key]    
    

def test_users_put_404(client):
    data = {'name': 'Viru'}
    response = client.put('/users/-1', data=json.dumps(data))
    
    assert response.status_code == 404
    assert isinstance(json.loads(response.data), dict)


def test_users_put_400(client, user):
    """this error will raise if client requests modify user_id, or date"""

    response = client.put('/users/{}'.format(user['id']), data=json.dumps({'id': 18, 'date': '12345'}))
    
    print(json.loads(response.data))    
    assert response.status_code == 400
    

def test_users_put_password_ok(client, user):
    response = client.put('/users/{}'.format(user['id']), data=json.dumps({'password': 'waterdog'}))
    assert response.status_code == 200

    response = client.get('/users/{}'.format(user['id']), data=json.dumps(['password']))
    assert json.loads(response.data)['password'] != 'waterdog'


############### delete test ###################

def test_users_delete(client, user):
    response = client.delete('/users/{}'.format(user['id']))    
    assert response.status_code == 200

    response = client.get('/users/{}'.format(user['id']), data=json.dumps([]))

    print(json.loads(response.data))    
    assert response.status_code == 404


def test_users_delete_404(client):
    response = client.delete('/users/-1')
    assert response.status_code == 404    

