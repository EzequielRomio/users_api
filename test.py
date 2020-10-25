import json

import requests

#r = requests.get('http://localhost:5000/users')

def create_test_enviroment():
    test_enviroment = {
        'name': 'TEST',
        'last_name': 'TEST_TEST',
        'email': 'TEST@perro.com',
        'date': 'none',
        'password': 'ehehehehhe'
    }    
    r_test = requests.post('http://localhost:5001/users', data=json.dumps(test_enviroment))
    return r_test.json()



######### TESTING POST ##########

def test_post():
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

def test_put_404():
    data = {'name': 'Viru'}
    
    r = requests.put('http://localhost:5001/users/0', data=json.dumps(data)) # user_id 0 not exist
    
    assert isinstance(r.json(), dict)
    assert r.status_code == 404
    print(r.json())
    print('test passed')
    
def test_put_password_ok():
    r_test = create_test_enviroment()

    data = {'password': 'waterdog'}
    r = requests.put('http://localhost:5001/users/{}'.format(r_test['id']), data=json.dumps(data))

    response = r.json()
    assert r.status_code == 200
    assert response['password'] != 'waterdog'
    print('test passed')

def test_put_ok():
    
    r_test = create_test_enviroment()

    data = {'name': 'Camila', 'last_name': 'grosso', 'email': 'camigrosso@gmail.com'}
    
    r = requests.put('http://localhost:5001/users/{}'.format(r_test['id']), data=json.dumps(data))
    
    user = r.json()
    r_test['id'] = str(r_test['id'])
    user['id'] = str(user['id'])
    
    for key in data.keys():
        if key == 'date':
            assert not data[key] == user[key]
        elif key != 'id':
            print(data[key], user[key])
            assert data[key] == user[key]
            assert user[key] != r_test[key]
        
    for key in user.keys():
        if key not in data:
            assert user[key] == r_test[key]    
    
    print(r.status_code)
    print(r.json())
    assert r.status_code == 200
     
    print('test passed')




######### TESTING GET ##########

def test_get_ok():
    r_test = create_test_enviroment()
    r = requests.get('http://localhost:5001/users/{}'.format(r_test['id']))
    user = r.json()
    #assert user.get('id') == str(r_test['id'])
    print(type(user))
    print(user)
    assert 'date' in user
    assert isinstance(user, dict)
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
    assert r.status_code == 200
    print('test passed')




test_put_ok()