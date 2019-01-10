import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY ASC NOT NULL, username text, password text)"
cursor.execute(create_table)

insert_query = "INSERT INTO users VALUES (1, 'test', 'testpassword')"
cursor.execute(insert_query)

connection.commit()
connection.close()
