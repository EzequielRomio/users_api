import os
import json

import pytest

os.environ['DATABASE'] = 'users_test.db'

#import create_data_base

from app import app
#from tests.test_users import client, user


# @pytest.fixture
# def prescription(client, user):
#     prescription = {
#         'user_id': user['id'],
#         'prescription_date': '00-00-2000',
#         'od': 'GRADUACION OD',
#         'oi': 'GRADUACION OI',
#         'addition': '5.00',
#         'notes': 'ametropia',
#         'doctor': 'EZEQUIEL ROMIO'
#     }

#     response = client.post('/prescriptions', data=json.dumps(prescription))
#     prescription['id'] = json.loads(response.data)['id']

#     yield prescription

#     client.delete('/prescriptions/{}'.format(prescription['id']))


############### post tests ############### 

def test_prescriptions_post(client, user):
    data = {
        'user_id': user['id'],
        'prescription_date': '17-08-2008',
        'od': 'ESF+2.00CIL-1.25*140',
        'oi': 'ESF+3.00',
        'addition': '2.25',
        'notes': 'ametropia',
        'doctor': 'Juan Abud'
    }
    response = client.post('/prescriptions', data=json.dumps(data))
    
    data['id'] = json.loads(response.data)['id']
    assert response.status_code == 200

    client.delete('/prescriptions/{}'.format(data['id']))


def test_prescriptions_post_404(client, prescription):
    """this error will raise if user_id is not valid"""
    prescription['user_id'] = -1

    response = client.post('/prescriptions', data=json.dumps(prescription))
    print(json.loads(response.data))
    
    assert response.status_code == 404


def test_prescriptions_post_400(client, prescription):
    # od is missing
    prescription.pop('od')
    response = client.post('/prescriptions', data=json.dumps(prescription))

    print(json.loads(response.data))
    assert response.status_code == 400


################### get tests ##################

def test_prescriptions_get(client, prescription):
    print(prescription['id'])

    response = client.get('/prescriptions/{}'.format(prescription['id']))
    
    assert response.status_code == 200
    response = json.loads(response.data)
    print(response)

    for k in prescription.keys():
        assert prescription[k] == response[k] 


def test_prescriptions_get_404(client):
    response = client.get('/prescriptions/-1')
    print(json.loads(response.data))
    assert response.status_code == 404


def test_get_prescriptions_by_user(client, user):    
    data = {
        'user_id': user['id'],
        'prescription_date': '27-09-88',
        'od': 'GET USER PRESCRIPTIONS TEST',
        'oi': 'GET USER PRESCRIPTIONS TEST',
        'addition': '2.25',
        'notes': 'ametropía',
        'doctor': 'Juan Abud'
    }

    prescriptions_ids = []
    for _ in range(3):
        response = client.post('/prescriptions', data=json.dumps(data))
        prescriptions_ids.append(json.loads(response.data)['id'])        

    response = client.get('/users/{}/prescriptions'.format(user['id']))        
    prescriptions = json.loads(response.data)
    print(prescriptions)
    assert response.status_code == 200
    assert len(prescriptions) == 3

    for id_number in prescriptions_ids:
        client.delete('/prescriptions/{}'.format(id_number))


################# put tests #################

def test_prescriptions_put_ok(client, prescription):
    data = {
        'od': 'od put ok',
        'oi': 'oi put ok',
        'addition': 'put ok',
    }

    response = client.put('/prescriptions/{}'.format(prescription['id']), data=json.dumps(data))
    assert response.status_code == 200

    response = client.get('/prescriptions/{}'.format(prescription['id']))
    
    prescription_updated = json.loads(response.data)

    for k in data.keys():
        print(k, ' tested')
        assert data[k] == prescription_updated[k] 
        assert prescription_updated[k] != prescription[k]


def test_prescriptions_put_400_modify_user(client, prescription):
    data = {'user_id': 4}

    response = client.put('/prescriptions/{}'.format(prescription['id']), data=json.dumps(data))
    print(json.loads(response.data))
    assert response.status_code == 400


def test_prescriptions_put_400_empty_data(client, prescription):
    response = client.put('/prescriptions/{}'.format(prescription['id']), data=json.dumps({}))
    print(json.loads(response.data))
    assert response.status_code == 400


############### delete tests ##################

def test_delete_prescription(client, prescription):
    response = client.delete('/prescriptions/{}'.format(prescription['id']))
    assert response.status_code == 200

    response = client.get('/prescriptions/{}'.format(prescription['id']), data=json.dumps([]))
    assert response.status_code == 404


def test_delete_prescription_404(client):
    response = client.delete('/prescriptions/-1')
    assert response.status_code == 404
