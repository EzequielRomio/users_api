import sqlite3


def sql_execute(query):
    conn = sqlite3.connect('users.db')

    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()


def sql_execute_get_list(query):
    conn = sqlite3.connect('users.db')

    cursor = conn.cursor()

    cursor.execute(query)

    result_list = [set_rows_columns_order(cursor, row) for row in cursor]
    conn.commit()
    
    return result_list


def sql_execute_post(query, row):
    conn = sqlite3.connect('users.db')

    c = conn.cursor()

    c.execute(query, row)   
    conn.commit()

    return c.lastrowid


def set_rows_columns_order(cursor, row):
    result = {}
    for idx, col in enumerate(cursor.description):
        result[col[0]] = row[idx]

    return result
