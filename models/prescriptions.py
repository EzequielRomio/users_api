import sqlite3

def get_prescriptions_by_user(user_id):
    query = 'SELECT * FROM prescriptions WHERE user_id = {}'.format(user_id)

    return sql_execute(query)


def sql_execute(query):
    conn = sqlite3.connect('users.db')

    cursor = conn.cursor()
    query = cursor.execute(query)
    conn.commit()
    return query.fetchall()
