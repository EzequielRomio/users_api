import sqlite3
import os
import argparse


ap = argparse.ArgumentParser()
ap.add_argument('-f', '--file', default='users.db')
args = ap.parse_args()


def execute_sql(sql_script):
    #conn = sqlite3.connect(args.file)
    conn = sqlite3.connect('users_test.db')
    with open('sqls/' + sql_script, 'r') as f:
        query = f.read()


    c = conn.cursor()
    c.execute(query)

    conn.commit()


if os.path.exists('users_test.db'):
    # always initialize tests with a new database
    os.remove('users_test.db')

for sql_script in sorted(os.listdir('sqls/')):
    execute_sql(sql_script)
