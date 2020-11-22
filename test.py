import json

import requests

#r = requests.get('http://localhost:5000/users')

def create_test_users():
    test_enviroment = {
        'name': 'TEST',
        'last_name': 'TEST_TEST',
        'email': 'TEST@test.com',
        'date': 'none',
        'password': 'test-test'
    }    
    r_test = requests.post('http://localhost:5001/users', data=json.dumps(test_enviroment))
    return r_test.json()

def create_test_prescriptions():
    user = create_test_users()
    data = {
        'user_id': user['id'],
        'prescription_date': '00-00-2000',
        'od': 'GRADUACION OD',
        'oi': 'GRADUACION OI',
        'addition': '5.00',
        'notes': 'ametropia',
        'doctor': 'EZEQUIEL ROMIO'
    }

    r = requests.post('http://localhost:5001/prescriptions', data=json.dumps(data))

    
    return r.json()


######### TESTING POST ##########

def test_post_user():
    data = {
        'name': 'pablo',
        'last_name': 'diaz_ogni',
        'email': 'pbldo@perro.com',
        'date': 'none',
        'password': 'ehehehehhe'
    }#   llamo con la funcion post#   #arg1=host          arg2=contenido
    r2 = requests.post('http://localhost:5001/users', data=json.dumps(data))
    # estoy pasando un pedido con la data del dict 

    #r2 guarda '<Response [200]>'
    
    response = r2.json()
    assert r2.status_code == 200
    assert 'id' in response 
    assert response['password'] != data['password']
    print('test passed')

def test_valid_post_name():
    #'name': 'pablo', FALTARÍA EL NOMBRE
    data = {
        'last_name': 'diaz_ogni',
        'email': 'pbldo@perro.com',
        'date': 'none',
        'password': 'ehehehehhe'
    }
    r2 = requests.post('http://localhost:5001/users', data=json.dumps(data))
    print(r2.json())
    assert r2.status_code == 400
    print('test passed')

def test_valid_post_mail():
    data = {
        'name': 'pablito',
        'last_name': 'diaz_ogni',
        'date': 'none',
        'password': 'ehehehehhe'
    }
    r2 = requests.post('http://localhost:5001/users', data=json.dumps(data))
    assert r2.status_code == 400
    print('test passed')



######### TESTING PUT ###########

def test_user_put_404():
    data = {'name': 'Viru'}
    
    r = requests.put('http://localhost:5001/users/0', data=json.dumps(data)) # user_id 0 not exist
    
    assert isinstance(r.json(), dict)
    assert r.status_code == 404
    print(r.json())
    print('test passed')
    
def test_user_put_password_ok():
    r_test = create_test_users()

    data = {'password': 'waterdog'}
    r = requests.put('http://localhost:5001/users/{}'.format(r_test['id']), data=json.dumps(data))

    response = r.json()
    assert r.status_code == 200
    assert response['password'] != 'waterdog'
    print('test passed')

def test_user_put_ok():
    
    r_test = create_test_users()
    
    data = {
        'name': 'Camila', 
        'last_name': 'Grosso', 
        'email': 'camilagros@etc.com', 
        'date': '2020-10-06 19:37:38',
        'password': 'k-1000-A'}
    
    for k, v in data.items():

        r = requests.put('http://localhost:5001/users/{}'.format(r_test['id']), data=json.dumps({k: v}))
        if k == 'date':
            assert r.status_code == 400
            continue
        assert r.status_code == 200
        user = r.json()
        print(user)
        
    for key in data.keys():
        if key == 'date':
            continue
        elif key == 'password':
            assert data[key] != user[key]
        elif key != 'id':
            print(data[key], user[key])
            assert data[key] == user[key]
    
    for key in user.keys():
        if key not in data:
            assert user[key] == r_test[key]    
    
     
    print('test passed')

def test_delete_user():
    r_test = create_test_users()
    print(r_test['id'])

    r = requests.delete('http://localhost:5001/users/{}'.format(r_test['id']))
    print(r.status_code)    
    assert r.status_code == 200

    r = requests.get('http://localhost:5001/users/{}'.format(r_test['id']))

    print(r.status_code)    
    assert r.status_code == 404
    
    print('test passed')

    
######### TESTING GET ##########

def test_user_get_ok():
    r_test = create_test_users()
    r = requests.get('http://localhost:5001/users/{}'.format(r_test['id']), data=json.dumps([]))
    user = r.json()
    #assert user.get('id') == str(r_test['id'])
    print(type(user))
    print(user)
    assert 'date' in user
    assert isinstance(user, dict)
    assert r.status_code == 200
    print(user)
    print('test passed')

    r = requests.get('http://localhost:5001/users/{}'.format(r_test['id']), data=json.dumps(['name', 'email']))
    user = r.json()

    assert 'password' not in user
    assert 'name' in user
    assert r.status_code == 200

    print(user)
    print('test passed')



def test_get_404():
    r = requests.get('http://localhost:5001/users/0')
    print(r.json())
    assert r.status_code == 404
    print(r.json())
    print('test passed')

def test_get_users_list():
    r = requests.get('http://localhost:5001/users')
    assert isinstance(r.json(), list)
    print(r.json())
    assert r.status_code == 200
    print('test passed')

def test_post_prescription():
    user = create_test_users()
    data = {
        'user_id': user['id'],
        'prescription_date': '17-08-2008',
        'od': 'ESF+2.00CIL-1.25*140',
        'oi': 'ESF+3.00',
        'addition': '2.25',
        'notes': 'ametropia',
        'doctor': 'Juan Abud'
    }

    r = requests.post('http://localhost:5001/prescriptions', data=json.dumps(data))
    response = r.json()
    print(response)
    print(response['id'])
    assert r.status_code == 200
     
    print('test passed')



def test_post_prescription_404():
    data = {
        'user_id': -1,
        'prescription_date': '17-08-2008',
        'od': 'ESF+2.00CIL-1.25*140',
        'oi': 'ESF+3.00',
        'addition': '2.25',
        'notes': 'ametropía',
        'doctor': 'Juan Abud'
    }

    r = requests.post('http://localhost:5001/prescriptions', data=json.dumps(data))
    print(r.status_code)
    
    assert r.status_code == 404
    print('test passed')

def test_get_prescription():
    prescript = create_test_prescriptions()
    print(prescript['id'])
    r = requests.get('http://localhost:5001/prescriptions/{}'.format(prescript['id']))
    response = r.json()
    print(response)
    assert r.status_code == 200
    
    
    for k in response.keys():
        assert prescript[k] == response[k] 
    
    print('test passed')

def test_get_prescription_404():
    r = requests.get('http://localhost:5001/prescriptions/-1')

    assert r.status_code == 404

    print('test_passed')


def test_delete_prescription():
    prescript = create_test_prescriptions()

    r = requests.delete('http://localhost:5001/prescriptions/{}'.format(prescript['id']))
    print(r.status_code)

    assert r.status_code == 200

    r = requests.get('http://localhost:5001/prescriptions/{}'.format(prescript['id']), data=json.dumps([]))

    assert r.status_code == 404

    print('test_passed')


def test_delete_prescription_404():
    r = requests.delete('http://localhost:5001/prescriptions/-1')

    assert r.status_code == 404

    print('test_passed')


def test_get_prescriptions_by_user():
    user = create_test_users()
    
    data = {
        'user_id': user['id'],
        'prescription_date': '27-09-88',
        'od': 'GET USER PRESCRIPTIONS TEST',
        'oi': 'GET USER PRESCRIPTIONS TEST',
        'addition': '2.25',
        'notes': 'ametropía',
        'doctor': 'Juan Abud'
    }

    for _ in range(3):
        r = requests.post('http://localhost:5001/prescriptions', data=json.dumps(data))        
        data['prescription_date'] += 'Test'
        print(r.status_code)
        print(r.json())

    r = requests.get('http://localhost:5001/users/{}/prescriptions'.format(user['id']))

    response = r.json()

    print(response)
    assert r.status_code == 200

    print('test_passed')

def test_put_prescription():
    prescription = create_test_prescriptions()
    
    data = {
        'od': 'od put ok',
        'oi': 'oi put ok',
        'addition': 'put ok',
    }

    r = requests.put('http://localhost:5001/prescriptions/{}'.format(prescription['id']), data=json.dumps(data))
    response = r.json()
    print(response)
    assert r.status_code == 200
    
    for k in data.keys():
        print(k, ' tested')
        assert data[k] == response[k] 
        assert response[k] != prescription[k]

    print('test passed')



def test_put_prescript_400():
    prescription = create_test_prescriptions()

    data = {'user_id': 4}

    r = requests.put('http://localhost:5001/prescriptions/{}'.format(prescription['id']), data=json.dumps(data))
    response = r.json()
    print(response)
    assert r.status_code == 400

    print('test passed')

"""
test_put_prescript_400()
test_delete_prescription_and_delete_404()

test_get_prescription_404()
test_post_prescription()
test_post_prescription_404()

test_post()
test_valid_post_mail()
test_valid_post_name()

test_put_404()

test_put_ok()
test_put_password_ok()
test_put_404()

"""
#test_user_get_ok()
#test_post_prescription()
#test_get_users_list()
#test_get_prescriptions_by_user()
#test_get_prescription()
#test_get_prescription_404()
#test_delete_user()
test_delete_prescription()