import sqlite3

conn=sqlite3.connect('uap/database/uap.db')
c = conn.cursor()

c.execute("DROP TABLE users")

#CRIADA TABLE USERS
c.execute("""CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL UNIQUE,
            pword TEXT NOT NULL,
            salt BINARY(32),
            file_path TEXT NOT NULL UNIQUE
            ) """)

conn.commit()
conn.close()
