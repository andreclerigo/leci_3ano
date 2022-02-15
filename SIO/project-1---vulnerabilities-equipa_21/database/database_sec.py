import sqlite3

conn=sqlite3.connect('database/forum_sec.db');
c = conn.cursor();

# c.execute("DROP TABLE users")
# c.execute("DROP TABLE posts")
# c.execute("DROP TABLE comments")

#CRIADA TABLE USERS
''' c.execute("""CREATE TABLE users (
            user_id INTEGER PRIMARY KEY,
            username TEXT NOT NULL UNIQUE,
            firstname TEXT NOT NULL,
            lastname TEXT NOT NULL,
            pword TEXT NOT NULL
            ) """)  '''

#CRIADA TABLE POSTS
''' c.execute("""CREATE TABLE posts (
            post_id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            msg TEXT NOT NULL,
            creator_id INTEGER,
            FOREIGN KEY(creator_id) REFERENCES users(user_id)
            ) """) '''

#CRIADA TABLE COMMENTS
''' c.execute("""CREATE TABLE comments (
            creator_id INTEGER NOT NULL,
            posted_id INTEGER NOT NULL,
            msg TEXT NOT NULL,
            FOREIGN KEY(creator_id) REFERENCES users(user_id),
            FOREIGN KEY(posted_id) REFERENCES posts(post_id)
            ) """) '''

#TESTER
# c.execute("INSERT INTO users VALUES(NULL,'Tiagura', 'Tiago', 'M', 'e6c3da5b206634d7f3f3586d747ffdb36b5c675757b380c6a5fe5c570c714349')")
# c.execute("INSERT INTO users(username, firstname, lastname, pword) VALUES('Hugito', 'Hugo', 'D', '1ba3d16e9881959f8c9a9762854f72c6e6321cdd44358a10a4e939033117eab9')")  
# c.execute("INSERT INTO users(username, firstname, lastname, pword) VALUES('Rager', 'Claudio', 'A', '3acb59306ef6e660cf832d1d34c4fba3d88d616f0bb5c2a9e0f82d18ef6fc167')") 
# c.execute("INSERT INTO users(username, firstname, lastname, pword) VALUES('CSGod', 'André', 'C', 'a417b5dc3d06d15d91c6687e27fc1705ebc56b3b2d813abe03066e5643fe4e74')")      

# c.execute("INSERT INTO posts(title, msg, creator_id) VALUES('1 question', 'How ya doing?', '4')")
# c.execute("INSERT INTO posts(title, msg, creator_id) VALUES('2 question', 'Should I Ragequit?', '3')")   
# c.execute("INSERT INTO posts(title, msg, creator_id) VALUES('3 question', 'Nerf JuanDeag?', '4')")    

# c.execute("INSERT INTO comments(creator_id, posted_id, msg) VALUES('1', '4', 'Amazing')")
# c.execute("INSERT INTO comments(creator_id, posted_id, msg) VALUES('1', '4', 'Nvm just broke with my gf')")
# c.execute("INSERT INTO comments(creator_id, posted_id, msg) VALUES('2', '2', 'Never give up')")

c.execute("SELECT * FROM comments WHERE posted_id='4' ")
for row in c:
    print('row = %r' % (row,))

conn.commit()
conn.close()
