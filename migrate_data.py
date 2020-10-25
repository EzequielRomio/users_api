import sqlite3
from app import USERS_FILE, get_users

conn = sqlite3.connect('users.db')

data = get_users(full_data=True)
data = [(x['name'], x['last_name'], x['email'], x['date'], x['password']) for x in data]
query = 'INSERT INTO users (name, last_name, email, date, password) VALUES (?, ?, ?, ?, ?)'


c = conn.cursor()
c.executemany(query, data)

conn.commit()