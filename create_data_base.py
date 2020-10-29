import sqlite3

conn = sqlite3.connect('users.db')

query = """CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    last_name TEXT, 
    email TEXT,
    date TEXT,
    password TEXT
);"""

c = conn.cursor()
c.executemany(query)

conn.commit()

