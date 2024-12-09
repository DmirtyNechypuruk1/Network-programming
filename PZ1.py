import sqlite3

conn = sqlite3.connect("pz.db")

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER)''')

# Додаємо новий запис
cursor.execute("INSERT INTO Users (username, email, age) VALUES ('newusers3', 'dmitry11@example.com', '23')")

res = cursor.execute("SELECT * FROM Users")

for row in res.fetchall():
    print(row)

conn.commit()
conn.close()
