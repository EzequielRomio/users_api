import sqlite3
from datetime import datetime
import hashlib

from models import sql_commands

def post_user(user):
    user['date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user['password'] = hash_password(user['password'])
    row = (
        user['name'], 
        user['last_name'],
        user['email'], 
        user['date'],
        user['password']
    )
    
    query = 'INSERT INTO users (name, last_name, email, date, password) VALUES (?, ?, ?, ?, ?)'

    user_id = sql_commands.sql_execute_post(query, row)

    return user_id


def get_user(user_id, fields=[]):
    """Returns the required user, with the respective fields"""
    if fields:
        fields_str = ', '.join(fields)
    else:
        fields_str = '*'

    query = "SELECT {} FROM users WHERE id = {}".format(fields_str, user_id) 

    query_result = sql_commands.sql_execute_get_list(query)

    if not query_result:
        return None

    user = query_result[0] # is a list with only one element; a dict with the requiered user 
    return user


def get_users(full_data=False):
    """Returns the list of users, if full_data adds password"""

    if full_data:
        query = 'SELECT * FROM users'
    else:
        query = 'SELECT id, name, last_name, email, date FROM users'

    query_result = sql_commands.sql_execute_get_list(query)

    return query_result


def modify_user(user_id, data_to_modify):
    if 'password' in data_to_modify:
        data_to_modify['password'] = hash_password(data_to_modify['password'])

    data_str_format = ', '.join(['{} = "{}"'.format(k, v) for k, v in data_to_modify.items()])

    query = 'UPDATE users SET {} WHERE id = {}'.format(data_str_format, user_id)

    sql_commands.sql_execute(query)


def delete_user(user_id):
    query = 'DELETE FROM users WHERE id={}'.format(user_id)
    sql_commands.sql_execute(query)


def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()

"""
TODO - get_user, and get_users in 1 function 
"""