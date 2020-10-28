import os
import json
import logging
from datetime import datetime
import hashlib


import sql_commands

from flask import Flask, request

USER_FIELDS = ('id','name', 'last_name', 'email', 'date', 'password')


class ServerError(Exception):
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

    return users_list

def search_user_by_id(id_number, users_list, valid_id=False):
    for user in users_list:
        if user['id'] == id_number or user['id'] == int(id_number):
            if valid_id:
                return True
            else:
                return user
    
    raise IdNotFoundError(id_number)

##########################################################


#################### PUT-METHODS #########################
@app.route('/delete/<user_id>', methods=['PUT'])
def delete_user(user_id):
    sql_commands.delete_user(user_id)
    return json.dumps(get_users())


@app.route('/modify/<user_id>', methods=['PUT'])
def users_put(user_id):
    users = get_users(full_data=True)
    data_to_modify = json.loads(request.data)
    data_to_modify.pop('id', None)
    data_to_modify.pop('date', None)
    try:
        user_modified = search_user_by_id(user_id, users)
        if 'password' in data_to_modify:
            data_to_modify['password'] = hash_password(data_to_modify['password'])
            
    except IdNotFoundError as e:
        return json.dumps({'Error': e.send_error_message()}), 404

    if not data_to_modify:
        return json.dumps({'Error': 'ERROR 400 "NO DATA TO MODIFY"'}), 400
    
    try:
        sql_commands.update_user_row(data_to_modify, user_id)

        for key in data_to_modify.keys():
            if data_to_modify[key] == user_modified['id']:
                raise ServerError
            
    except ServerError:
        return json.dumps({'Error': 'Server problem'}), 500

    
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
            
            sql_response = sql_commands.post_new_user(user)
                            
            for value in sql_response[0]:
                if isinstance(value, int):
                    user['id'] = value
            #app.logger.info('USERS RESULT:\n\n{}'.format(user))
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



def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()

def valid_id_number(id_number):
    if not sql_commands.get_user_by_row('*', id_number):
        return False
    else:
        return True
