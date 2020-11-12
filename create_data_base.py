import sqlite3

sql_script = 'sqls/' + '' # Complete with the file's name 

conn = sqlite3.connect('users.db')

with open(sql_script, 'r') as f:
    query = ''
    for line in f:
        print(line)
        query += line


c = conn.cursor()
c.execute(query)

conn.commit()

