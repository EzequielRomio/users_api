#from main.sql_commands import sql_commands

import json

def get_user(user_id, fields=[]):
    """Returns the required user, with the respective fields"""
    query_result = get_user(user_id, fields)

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

    return json.dumps(user)


def get_users(full_data=False):
    """Returns the list of users, if full_data adds password"""
    query_result = get_users(full_data=full_data)
    
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
        
        for ix in range(user_values):
            user[fields[ix]] = user_values[ix]
        
        users_list.append(user)
    
    return users_list