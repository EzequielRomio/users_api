import sqlite3



def get_users_parse(cursor, row):
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


def get_users(full_data=False):

    if full_data:
        query_command = 'SELECT * FROM users'
    else:
        query_command = 'SELECT id, name, last_name, email, date FROM users'

    conn = sqlite3.connect('users.db')


    cursor = conn.cursor()
    cursor.execute(query_command)
    #query = cursor.execute(query_command)
    
    conn.commit()
    return cursor.fetchall



# will delete
def get_users_list(full_data=False):

    if full_data:
        query_command = 'SELECT * FROM users'
    else:
        query_command = 'SELECT id, name, last_name, email, date FROM users'

    conn = sqlite3.connect('users.db')


    cursor = conn.cursor()
    query = cursor.execute(query_command)

    users_list = [get_users_parse(cursor, user) for user in query]
    conn.commit()
    return users_list


def get_user(user_id, fields=[]):
    if fields:
        fields_str = ', '.join(fields)
    else:
        fields_str = '*'
    query = "SELECT {} FROM users WHERE id = {}".format(fields_str, user_id,)

    conn = sqlite3.connect('users.db')

    cursor = conn.cursor()
    query = cursor.execute(query)
    conn.commit()
    return query.fetchall()


# will delete 
def get_user_by_row(rows, id_number):
    if rows != '*':
        rows = set_str_format(rows)

    query_command = 'SELECT {} FROM users WHERE id = {}'.format(rows, id_number)

    conn = sqlite3.connect('users.db')

    cursor = conn.cursor()
    query = cursor.execute(query_command)
    conn.commit()
    return query.fetchall()



def update_user(id_number, new_data):

    data_str_format = ', '.join(['{} = "{}"'.format(k, v) for k, v in new_data.items()])

    query_command = 'UPDATE users SET {} WHERE id = {}'.format(data_str_format, id_number)

    
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
    row = (
        user['name'], 
        user['last_name'],
        user['email'], 
        user['date'], 
        user['password']
    )
    #data = [(x['name'], x['last_name'], x['email'], x['date'], x['password']) for x in data]
    query = 'INSERT INTO users (name, last_name, email, date, password) VALUES (?, ?, ?, ?, ?)'

    conn = sqlite3.connect('users.db')

    c = conn.cursor()

    c.execute(query, row)   
    conn.commit()

    return c.lastrowid





######################################################################
###################### PRESCRIPTIONS TABLE ###########################

"""
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    prescription_date TEXT NOT NULL,
    created_date TEXT NOT NULL, 
    od TEXT NOT NULL,
    oi TEXT NOT NULL,
    addition TEXT,
    notes TEXT,
    doctor TEXT   
"""

def post_prescription(data):
    row = (
        data['user_id'], 
        data['prescription_date'], 
        data['created_date'], 
        data['od'], 
        data['oi'], 
        data['addition'], 
        data['notes'], 
        data['doctor']
    )
    query = 'INSERT INTO prescriptions (user_id, prescription_date, created_date, od, oi, addition, notes, doctor) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'

    conn = sqlite3.connect('users.db')

    c = conn.cursor()
    c.executemany(query, [row])
        
    conn.commit()

    prescript_id = [n for n in (c.execute('SELECT MAX(id) FROM prescriptions'))] 

    return get_prescription(prescript_id[0][0])


def get_prescription(prescription_id):
    query = 'SELECT * FROM prescriptions WHERE id = {}'.format(prescription_id)

    conn = sqlite3.connect('users.db')

    cursor = conn.cursor()
    query = cursor.execute(query)
    conn.commit()
    return query.fetchall()

def get_prescriptions_ids():
    query = 'SELECT id FROM prescriptions'

    conn = sqlite3.connect('users.db')

    cursor = conn.cursor()
    query = cursor.execute(query)
    conn.commit()

    return query.fetchall()

def get_prescription_row(prescription_id, row):
    query_command = 'SELECT {} FROM prescriptions WHERE id = {}'.format(row, prescription_id)

    conn = sqlite3.connect('users.db')

    cursor = conn.cursor()
    query = cursor.execute(query_command)
    conn.commit()
    return query.fetchall()

def get_prescriptions_by_user(user_id):
    query_command = 'SELECT * FROM prescriptions WHERE user_id = {}'.format(user_id)

    conn = sqlite3.connect('users.db')

    cursor = conn.cursor()
    query = cursor.execute(query_command)
    conn.commit()
    return query.fetchall()


def modify_prescription(prescription_id, new_data):

    data_str_format = ', '.join(['{} = "{}"'.format(k, v) for k, v in new_data.items()])

    query = 'UPDATE prescriptions SET {} WHERE id = {}'.format(data_str_format, prescription_id)

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)

    conn.commit()



def delete_prescription(prescription_id):
    query_command = 'DELETE FROM prescriptions WHERE id={}'.format(prescription_id)
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query_command)

    conn.commit()

    