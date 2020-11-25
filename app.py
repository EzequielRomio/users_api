import os
import json
import logging

from flask import Flask, request

from models import users, prescriptions


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
    return json.dumps(users.get_users(full_data=full_data))


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
            
            return json.dumps(result)
        else:
            raise IdNotFoundError(user_id)

    except IdNotFoundError as e:
        return json.dumps({'Error': e.send_error_message()}), 404    


################################################ DELETE-METHODS #####################################################

######################## USERS ##########################
@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        if not users.get_user(user_id):
            raise IdNotFoundError(user_id)
        
        users.delete_user(user_id)
        return {}

    except IdNotFoundError as e:
        return json.dumps({'Error': e.send_error_message()}), 404

#########################################################

################## PRESCRIPTIONS ########################
@app.route('/prescriptions/<prescription_id>', methods=['DELETE'])
def delete_prescript(prescription_id):
    try:
        prescription = prescriptions.get_prescription(prescription_id)
        if not prescription:
            raise IdNotFoundError(prescription_id)
        else:
            prescriptions.delete_prescription(prescription_id)
            return {}

    except IdNotFoundError as e:
        return json.dumps({'Error': e.send_error_message()}), 404

#########################################################

################################################### PUT-METHODS ####################################################

####################### USERS ##########################
@app.route('/users/<user_id>', methods=['PUT'])
def put_user(user_id):
    try:
        if not users.get_user(user_id):
            raise IdNotFoundError(user_id)
        
        data_to_modify = json.loads(request.data)
        data_to_modify.pop('id', None)
        data_to_modify.pop('date', None)

        if not data_to_modify:
            return json.dumps({'Error': 'ERROR 400 "NO DATA TO MODIFY"'}), 400 

        users.modify_user(user_id, data_to_modify)
        return {}

    except IdNotFoundError as e:
        return json.dumps({'Error': e.send_error_message()}), 404

##############################################################

####################### PRESCRIPTIONS ########################
@app.route('/prescriptions/<prescription_id>', methods=['PUT'])
def put_prescription(prescription_id):
    try:
        if not prescriptions.get_prescription(prescription_id):
            raise IdNotFoundError(prescription_id)

        data_to_modify = json.loads(request.data)
        data_to_modify.pop('id', None)
        data_to_modify.pop('created_date', None)

        if not data_to_modify:
            return json.dumps({'Error': 'ERROR 400 "NO DATA TO MODIFY"'}), 400

        if 'user_id' in data_to_modify:
            return json.dumps({'Error': 'ERROR 400 "CANNOT MODIFY USER_ID, DELETE PRESCRIPTION AND CREATE A NEW ONE"'}), 400

        prescriptions.modify_prescription(prescription_id, data_to_modify)
        return {}    

    except IdNotFoundError as e:
        return json.dumps({'Error': e.send_error_message()}), 404


###################################################### POST-METHODS #############################################################

######################### USERS ##############################
@app.route('/users', methods=['POST'])
def post_user():
    user = json.loads(request.data)
    try:
        if validate_user_body(user):
            user_id = users.post_user(user)
            return json.dumps({'id': user_id})

    except MissingFieldError as e:
        app.logger.debug(e.send_error_message())
        return json.dumps({'Error': e.send_error_message()}), 400


def validate_user_body(data):
    for field in ('name', 'email'):
        if not field in data.keys():
            app.logger.debug(field)
            raise MissingFieldError(field)
    return True


######################################################

################## PRESCRIPTIONS #####################
@app.route('/prescriptions', methods=['POST'])
def prescription_post():
    prescription = json.loads(request.data)
    try:
        if 'user_id' not in prescription:
            raise MissingFieldError('user_id')
        
        if not users.get_user(prescription['user_id']):
            raise IdNotFoundError(prescription['user_id'])

        if validate_prescription_body(prescription):
            prescription_id = prescriptions.post_prescription(prescription)
            return json.dumps({'id': prescription_id})

    except IdNotFoundError as e:
        app.logger.debug(e.send_error_message())
        return json.dumps({'Error': e.send_error_message()}), 404

    except MissingFieldError as e:
        app.logger.debug(e.send_error_message())
        return json.dumps({'Error': e.send_error_message()}), 400


def validate_prescription_body(data):
    for field in ('user_id', 'prescription_date', 'od', 'oi'):
        if not field in data.keys():
            app.logger.info(field)
            raise MissingFieldError(field)
    return True
