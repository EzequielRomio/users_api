
"""
def get_users(full_data=False):
    if full_data:
        users_list = sql_commands.get_users_list(full_data=True)
    else:
        users_list = sql_commands.get_users_list()

    return users_list


def user_get(user_id):
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
"""