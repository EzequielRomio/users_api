# para correr reuqeriment tirar pip install -r nombredearchivo
import os
import json
import logging
from datetime import datetime
import hashlib


import sql_commands

from flask import Flask, request


USERS_FILE = os.path.abspath(os.environ.get('USERS_FILE', 'users.csv'))
ID_FILE = os.path.abspath(os.environ.get('ID_FILE', 'settings.json'))
USER_FIELDS = ('id','name', 'last_name', 'email', 'date', 'password')


if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, 'w'):
        pass

if not os.path.exists(ID_FILE):
    with open(ID_FILE, 'w'):
        pass



class RequirementError(Exception):
    pass

class MissingFieldError(RequirementError):
    def send_error_message(self):
        return "400 < {} > FIELD IS MISSING".format(self.args[0])

class IdNotFoundError(RequirementError):
    def send_error_message(self):
        return "404 < {} > ID NUMBER NOT FOUND".format(self.args[0])



app = Flask('users_api')

LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO').upper()

logging.basicConfig(level=getattr(logging, LOG_LEVEL))

app.logger.info('The API is running!')

################# GET-METHODS ##################

@app.route('/users', methods=['GET'])
def users_get():
    #app.logger.debug(json.dumps(get_users()))
    return json.dumps(get_users())


@app.route('/users/<user_id>', methods=['GET'])
def user_get(user_id):
    #users_list = get_users()
    try:
        user_data = sql_commands.get_user_by_row(rows='*', id_number=user_id)

        if not user_data:
            raise IdNotFoundError(user_id)

        user = {}
        user['id'] = user_data[0][0]
        user['name'] = user_data[0][1]
        user['last_name'] = user_data[0][2]
        user['email'] = user_data[0][3]
        user['date'] = user_data[0][4]

        return json.dumps(user)
        #return json.dumps(search_user_by_id(user_id, users_list))
    except IdNotFoundError as e:
        return json.dumps({'Error': e.send_error_message()}), 404

def get_users(full_data=False):
    if full_data:
        users_list = sql_commands.get_users_list(full_data=True)
    else:
        users_list = sql_commands.get_users_list()
    """
    users_list = []
    with open(USERS_FILE, 'r') as f:
        for line in f:
            row = line.strip().split(',', 5)
            users_list.append({
                'id': row[0],
                'name': row[1],
                'last_name': row[2],
                'email': row[3],
                'date': row[4],
            })
            if full_data:
                users_list[-1]['password'] = row[5]
    """
    return users_list

"""
def get_user_id():
    
    with open(ID_FILE, 'r') as f:
        data = json.load(f)
    return data['last_id'] + 1
"""
def search_user_by_id(id_number, users_list):
    for user in users_list:
        if user['id'] == id_number or user['id'] == int(id_number):
            return user
    
    raise IdNotFoundError(id_number)

##########################################################


#################### PUT-METHODS #########################

@app.route('/users/<user_id>', methods=['PUT'])
def users_put(user_id):
    users = get_users(full_data=True)
    data_to_modify = json.loads(request.data)
    data_to_modify.pop('id', None)
    data_to_modify.pop('date', None)
    try:
        user_to_modify = search_user_by_id(user_id, users)
        if 'password' in data_to_modify:
            data_to_modify['password'] = hash_password(data_to_modify['password'])
        user_to_modify.update(data_to_modify)
            
    except IdNotFoundError as e:
        return json.dumps({'Error': e.send_error_message()}), 404

    sql_response = sql_commands.update_user_row(user_to_modify, user_id)
    print(sql_response)
    user_modified = {}
    for ix, value in enumerate(sql_response):
        if USER_FIELDS[ix] == 'password' and 'password' not in data_to_modify:
            continue

        user_modified[USER_FIELDS[ix]] = value
    
    
    """
    with open(USERS_FILE, 'w') as f:
        for user in users:
            f.write(','.join([str(user[k]) for k in USER_FIELDS]))
            f.write('\n')
    """
    return json.dumps(user_modified)  

##############################################################


####################### POST-METHODS #########################

@app.route('/users', methods=['POST'])
def user_post():
    print(request.data)
    user = json.loads(request.data)
    try:
        if valid_request(user):
            user['date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            user['password'] = hash_password(user['password'])
            #save_user(user)
            sql_response = sql_commands.post_new_user(user)
            
            for value in sql_response[0]:
                if isinstance(value, int):
                    user['id'] = value
            return json.dumps(user)

    except MissingFieldError as e:
        app.logger.debug(e.send_error_message())
        return json.dumps({'Error': e.send_error_message()}), 400

def valid_request(data):
    for header in ('name', 'email'):
        if not header in data.keys():
            app.logger.debug(header)
            raise MissingFieldError(header)
    return True

def save_user(data):
    with open(USERS_FILE, 'a') as f:
        f.write(','.join([str(data[k]) for k in USER_FIELDS]))
        f.write('\n')

    id_data = {'last_id': data['id']}
    with open(ID_FILE, 'w') as f:
        f.write(json.dumps(id_data))


def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()

def valid_id_number(id_number):
    if not sql_commands.get_user_by_row('*', id_number):
        return False
    else:
        return True


#################################################################





"""
TODO - si no tiene los campos rekeridos (nombre o email), devolver un 400 + mensaje 'necesitas el campo rekerido tal...'
TODO - levantar el datetime Y DEVOLVERLO EN EL POSTO O GET O PUT O LOQ SEA
TODO - implementar el PUT /users/id PASAR UN JSON CON REQUERIMIENTO EJEMPLO NOMBRE, Y VA A MODIFICAR ESO CON EL VALOR NUEVO
TODO - SI EL USUARIO NO EXISTE DEVOLVER UN 404
TODO - crear test para post, para put, para post q devuelve 400, y para get
TODO - RENOMBRAR HEADERS
- RENOMBRAR SETTINGS.JSON STAMPS POR EJEMPLO 

TODO - HASHEAR LA PASS
TODO - CON EL TEST Q CREA AL USUARIO, Q CHEKEE SI LA PASS ESTA HASHEADA
TODO - DEJAR EL ID EN UNA SOLA FUNCION
TODO - GET_USER/USERS_FULL_DATA EN UNA SOLA FUNCION, VALE (full_data=False)
TODO - EL SAVE_USER DEBE GUARDAR EL ID EN EL JSON (O SEA TOD O EN LA MISMA FUNCION)
- el test levante el users_test.csv y que compruebe ahi si la conatreseña cambio, y que deje de devolverlo el post
"""