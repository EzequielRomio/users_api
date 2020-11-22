import json
import sqlite3


def get_user(user_id, fields=[]):
    """Returns the required user, with the respective fields"""
    if fields:
        fields_str = ', '.join(fields)
    else:
        fields_str = '*'

    query = "SELECT {} FROM users WHERE id = {}".format(fields_str, user_id) 

    #query = "SELECT * FROM users WHERE id = 17"
    query_result = sql_execute(query)

    if not query_result:
        return None

    user = {}
    if not fields:
        user['id'] = query_result[0][0]
        user['name'] = query_result[0][1]
        user['last_name'] = query_result[0][2]
        user['email'] = query_result[0][3]
        user['date'] = query_result[0][4]
    else:
        for ix, field in enumerate(fields):
            user[field] = query_result[0][ix]

    return user


def get_users(full_data=False):
    """Returns the list of users, if full_data adds password"""

    if full_data:
        query = 'SELECT * FROM users'
    else:
        query = 'SELECT id, name, last_name, email, date FROM users'


    query_result = sql_execute(query)
    
    fields = (
        'id',
        'name',
        'last_name',
        'email',
        'date',
        'password'
    )

    users_list = []
    for user_values in query_result:
        user = {}
        
        if full_data:
            user['password'] = user_values[5]
        
        for ix in range(len(user_values)):
            user[fields[ix]] = user_values[ix]
        
        users_list.append(user)
    
    return users_list


def delete_user(id_number):
    query = 'DELETE FROM users WHERE id={}'.format(id_number)
    sql_execute(query)


#################################################################
#                                                               #
##########################    SQL    ############################

def sql_execute(query):
    conn = sqlite3.connect('users.db')

    cursor = conn.cursor()

    cursor.execute(query)
    
    conn.commit()
    return cursor.fetchall()
