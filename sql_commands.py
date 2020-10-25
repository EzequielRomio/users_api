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
    for row in new_data.keys():
        value = new_data[row]

    query_command = 'UPDATE users SET {} = "{}" WHERE id = {}'.format(row, value, id_number)
    
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = cursor.execute(query_command)

    conn.commit()
    return query.fetchall()


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
 



"""
x = get_user_by_row(rows='*', id_number=0)
print(x)
print(x == True)
print(x is None)
print(bool(x))

print(update_user_row('name', 'waterdog', 8))

user = {'name': 'PEPITO', 'last_name': 'ROMIO', 'email': 'VIRUK-PO@GMAIL.COM', 'date': 'martes 8/9 a las 15', 'password': 'jdsnfssdnlksij998h'}
print(save_new_user(user))
print(show_users())



print()
print(show_users(full_data=True))
"""
"""
for x in range(1, 16):
    print(get_user_by_row(['name', 'last_name'], id_number=x))
"""
