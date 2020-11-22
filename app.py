import os
import json
import logging
from datetime import datetime
import hashlib

from models import users, prescriptions
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

############################################# GET-METHODS ###########################################################

####################### USERS ####################### 
@app.route('/users', methods=['GET'])
def get_users(full_data=False):
    if full_data:
        return json.dumps(users.get_users(full_data=True))
    else:
        return json.dumps(users.get_users())


@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    fields = json.loads(request.data)
    
    try:
        user_data = users.get_user(user_id, fields)

        if not user_data:
            raise IdNotFoundError(user_id)

        return json.dumps(user_data)

    except IdNotFoundError as e:
        return json.dumps({'Error': e.send_error_message()}), 404


##########################################################


##################### PRESCRIPTIONS ######################

@app.route('/prescriptions/<prescription_id>', methods=['GET'])
def get_prescription(prescription_id):
    try:
        prescription = prescriptions.get_prescription(prescription_id)

        if not prescription:
            raise IdNotFoundError(prescription_id)

        return json.dumps(prescription)
        
    except IdNotFoundError as e:
        return json.dumps({'Error': e.send_error_message()}), 404


@app.route('/users/<user_id>/prescriptions', methods=['GET'])
def get_user_prescriptions(user_id):
    try:
        if users.get_user(user_id):
            result = prescriptions.get_prescriptions_by_user(user_id)
            
            return json.dumps({'results': result})

    except IdNotFoundError as e:
        return json.dumps({'Error': e.send_error_message()}), 404    


################################################ DELETE-METHODS #####################################################

######################## USERS ##########################
@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):


    sql_commands.delete_user(user_id)
    return json.dumps(get_users())
#########################################################

################## PRESCRIPTIONS ########################
@app.route('/prescriptions/<prescription_id>', methods=['DELETE'])
def delete_prescript(prescription_id):
    try:
        prescription = sql_commands.get_prescription(prescription_id)

        if not prescription:
            raise IdNotFoundError(prescription_id)
        else:
            sql_commands.delete_prescription(prescription_id)
            return {}

    except IdNotFoundError as e:
        return json.dumps({'Error': e.send_error_message()}), 404

#########################################################


################################################### PUT-METHODS ####################################################

####################### USERS ##########################
@app.route('/users/<user_id>', methods=['PUT'])
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
        sql_commands.update_user(data_to_modify, user_id)

        for key in data_to_modify.keys():
            if data_to_modify[key] == user_modified['id']:
                raise ServerError
            
    except ServerError:
        return json.dumps({'Error': 'Server problem'}), 500

    app.logger.info(user_modified)
    return json.dumps(user_modified)  

##############################################################

####################### PRESCRIPTIONS ########################
@app.route('/prescriptions/<prescription_id>', methods=['PUT'])
def put_prescription(prescription_id):
    data_to_modify = json.loads(request.data)
    data_to_modify.pop('id', None)
    data_to_modify.pop('created_date', None)

    if not data_to_modify:
        return json.dumps({'Error': 'ERROR 400 "NO DATA TO MODIFY"'}), 400

    if 'user_id' in data_to_modify:
        return json.dumps({'Error': 'ERROR 400 "CANNOT MODIFY USER_ID, DELETE PRESCRIPTION AND CREATE A NEW ONE"'}), 400
    

    try:
        #if validate_prescript_id(prescription_id):
        sql_commands.modify_prescription(prescription_id, data_to_modify)
        return get_prescription(prescription_id)

    except IdNotFoundError as e:
        return json.dumps({'Error': e.send_error_message()}), 404



###################################################### POST-METHODS #############################################################

######################### USERS ##############################
@app.route('/users', methods=['POST'])
def user_post():
    print(request.data)
    user = json.loads(request.data)
    try:
        if validate_user_body(user):
            user['date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            user['password'] = hash_password(user['password'])
            
            user['id'] = sql_commands.post_new_user(user)
             
            #app.logger.info('USERS RESULT:\n\n{}'.format(user))
            return json.dumps(user)

    except MissingFieldError as e:
        app.logger.debug(e.send_error_message())
        return json.dumps({'Error': e.send_error_message()}), 400

######################################################

################## PRESCRIPTIONS #####################
@app.route('/prescriptions', methods=['POST'])
def prescription_post():
    prescription = json.loads(request.data)
    try:
        if validate_prescription_body(prescription) and valid_id_number(prescription['user_id']): 
            prescription['created_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            sql_response = sql_commands.post_prescription(prescription)

            id_got = False                
            for value in sql_response[0]:
                if not id_got:
                    prescription['id'] = value
                    id_got = True
            app.logger.debug('USERS RESULT:\n\n{}'.format(prescription))
            return json.dumps(prescription)

    except MissingFieldError as e:
        app.logger.debug(e.send_error_message())
        return json.dumps({'Error': e.send_error_message()}), 400

    except IdNotFoundError as e:
        app.logger.debug(e.send_error_message())
        return json.dumps({'Error': e.send_error_message()}), 404


#######################################################################

def validate_user_body(data):
    for field in ('name', 'email'):
        if not field in data.keys():
            app.logger.debug(field)
            raise MissingFieldError(field)
    return True

def validate_prescription_body(data):
    for field in ('user_id', 'prescription_date', 'od', 'oi'):
        if not field in data.keys():
            app.logger.info(field)
            raise MissingFieldError(field)
    return True
        
def validate_prescript_id(prescript_id):
    ids = [number for number in sql_commands.get_prescriptions_ids()]
    app.logger.info(ids)
    if not prescript_id in ids:
        raise IdNotFoundError(prescript_id)
    else:
        return True


def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()

def valid_id_number(id_number):
    if not sql_commands.get_user_by_row('*', id_number):
        raise IdNotFoundError(id_number)
    else:
        return True

