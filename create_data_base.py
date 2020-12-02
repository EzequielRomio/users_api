import sqlite3
import os
import argparse

ap = argparse.ArgumentParser()
ap.add_argument('-f', '--file', default='users.db')
args = ap.parse_args()

#sql_script = 'sqls/' + '01_initial_db.sql'
#sql_script = 'sqls/' + '02_prescription_table.sql' # Complete with the file's name 

def execute_sql(sql_script):
    conn = sqlite3.connect(args.file)

    with open('sqls/' + sql_script, 'r') as f:
        query = f.read()


    c = conn.cursor()
    c.execute(query)

    conn.commit()


for sql_script in sorted(os.listdir('sqls/')):
    execute_sql(sql_script)


