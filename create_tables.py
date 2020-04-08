import sqlite3

connection = sqlite3.connect("data.db")  # SQLite DB

cursor = connection.cursor()
create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

insert_query = "INSERT INTO users VALUES (?, ?, ?)"
users = [(1, 'przemek','qazwsx123'), (2, 'denis','qazwsx123'),
(3, 'siek', 'qazwsx123')]
cursor.executemany(insert_query, users)

create_table = "CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name text, price real)"
cursor.execute(create_table)


connection.commit()
connection.close()