import sqlite3

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


def sql_execute(query):
    conn = sqlite3.connect('users.db')

    cursor = conn.cursor()
    query = cursor.execute(query)
    conn.commit()
    return query.fetchall()
