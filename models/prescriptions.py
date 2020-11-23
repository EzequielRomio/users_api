import sqlite3
from datetime import datetime

def post_prescription(prescription):
    prescription['created_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = (
        prescription['user_id'], 
        prescription['prescription_date'], 
        prescription['created_date'], 
        prescription['od'], 
        prescription['oi'], 
        prescription['addition'], 
        prescription['notes'], 
        prescription['doctor']
    )
    query = 'INSERT INTO prescriptions (user_id, prescription_date, created_date, od, oi, addition, notes, doctor) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'

    prescription_id = sql_execute_post(query, row)

    return prescription_id


def get_prescription(prescription_id):
    """Returns the required prescription"""

    query = "SELECT * FROM prescriptions WHERE id = {}".format(prescription_id) 

    query_result = sql_execute(query)

    if not query_result:
        return None

    prescription = {
        'id': query_result[0][0],
        'user_id': query_result[0][1],
        'prescription_date': query_result[0][2],
        'created_date': query_result[0][3],
        'od': query_result[0][4],
        'oi': query_result[0][5],
        'addition': query_result[0][6],
        'notes': query_result[0][7],
        'doctor': query_result[0][8]
    }

    return prescription


def get_prescriptions_by_user(user_id):
    query = 'SELECT * FROM prescriptions WHERE user_id = {}'.format(user_id)

    return sql_execute(query)


def modify_prescription(prescription_id, data_to_modify):

    data_str_format = ', '.join(['{} = "{}"'.format(k, v) for k, v in data_to_modify.items()])

    query = 'UPDATE prescriptions SET {} WHERE id = {}'.format(data_str_format, prescription_id)

    sql_execute(query)



def delete_prescription(prescription_id):
    query = 'DELETE FROM prescriptions WHERE id={}'.format(prescription_id)
    sql_execute(query)


################### sql ####################
def sql_execute(query):
    conn = sqlite3.connect('users.db')

    cursor = conn.cursor()
    query = cursor.execute(query)
    conn.commit()
    return query.fetchall()


def sql_execute_post(query, row):
    conn = sqlite3.connect('users.db')

    c = conn.cursor()

    c.execute(query, row)   
    conn.commit()

    return c.lastrowid
