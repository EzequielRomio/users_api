import sqlite3



def get_users(cursor, row):
    users = {}
    for idx, col in enumerate(cursor.description):
        users[col[0]] = row[idx]

    return users


def set_str_format(rows):
    rows_str_format = ''
    for ix, row in enumerate(rows):
        if ix == (len(rows) - 1):
            rows_str_format += row
        else:
            rows_str_format += row + ', ' 

    return rows_str_format



def get_users_list(full_data=False):

    if full_data:
        query_command = 'SELECT * FROM users'
    else:
        query_command = 'SELECT id, name, last_name, email, date FROM users'

    conn = sqlite3.connect('users.db')


    cursor = conn.cursor()
    query = cursor.execute(query_command)

    users_list = [get_users(cursor, user) for user in query]
    conn.commit()
    return users_list


def get_user_by_row(rows, id_number):
    if rows != '*':
        rows = set_str_format(rows)

    query_command = 'SELECT {} FROM users WHERE id = {}'.format(rows, id_number)

    conn = sqlite3.connect('users.db')

    cursor = conn.cursor()
    query = cursor.execute(query_command)
    conn.commit()
    return query.fetchall()



def update_user_row(new_data, id_number):
    for k, v in new_data.items():
        row = k
        value = v

    query_command = 'UPDATE users SET {} = "{}" WHERE id = {}'.format(row, value, id_number)
    
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query_command)

    conn.commit()

def delete_user(id_number):
    query_command = 'DELETE FROM users WHERE id={}'.format(id_number)
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query_command)

    conn.commit()

 


def post_new_user(user):
    data = [(user['name'], user['last_name'],user['email'], user['date'], user['password'])]
    #data = [(x['name'], x['last_name'], x['email'], x['date'], x['password']) for x in data]
    query = 'INSERT INTO users (name, last_name, email, date, password) VALUES (?, ?, ?, ?, ?)'

    conn = sqlite3.connect('users.db')

    c = conn.cursor()
    c.executemany(query, data)
        
    conn.commit()

    id_number = [n for n in (c.execute('SELECT MAX(id) FROM users'))] 
    
    return get_user_by_row('*', id_number[0][0])
 