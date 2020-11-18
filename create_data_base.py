import sqlite3

sql_script = 'sqls/' + '02_prescription_table.sql' # Complete with the file's name 

"""
for sql_script in sorted(os.listdir('sqls/')):
    execute_sql(sql_script)
"""


conn = sqlite3.connect('users.db')

with open(sql_script, 'r') as f:
    query = f.read()



c = conn.cursor()
c.execute(query)

conn.commit()

