import sqlite3

conn=sqlite3.connect('database/forum_sec.db')
c = conn.cursor()

# c.execute("DROP TABLE users")
# c.execute("DROP TABLE posts")
# c.execute("DROP TABLE comments")

#CRIADA TABLE USERS
''' c.execute("""CREATE TABLE users (
            user_id INTEGER PRIMARY KEY,
            username TEXT NOT NULL UNIQUE,
            firstname TEXT NOT NULL,
            lastname TEXT NOT NULL,
            pword TEXT NOT NULL,
            salt BINARY(32),
            auth_token TEXT,
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
# c.execute("INSERT INTO users(username, firstname, lastname, pword, salt) VALUES('Tiagura', 'Tiago', 'M', '9868b0ccfdad4e659adc783394050e79368c32a3d13866635eeda64c89eab05d', 'T5VeeoYe0Iu6+pAvX5IqUIDzqqMD/pmjFVTdIowbSOA=')")
# c.execute("INSERT INTO users(username, firstname, lastname, pword, salt) VALUES('Hugito', 'Hugo', 'D', 'ea3dfcee7068466f776fe7fa1dc66913970af4131b503db3501982103480ef44', 'KnuCxmo2tK4SkwmgFmZyErNW3YEajb2jxQ7uxX99yzA=')")  
# c.execute("INSERT INTO users(username, firstname, lastname, pword, salt) VALUES('Rager', 'Claudio', 'A', 'da60df21b39eaefff299ade986ad92308e3a0deea1d67414283d2e1f44c2ffa1', 'kjsFZ7p9E1Nrd6fDKXK8UqODIoE89nI5qUQbo11sTZM=')") 
# c.execute("INSERT INTO users(username, firstname, lastname, pword, salt) VALUES('CSGod', 'André', 'C', '5e20e56a303ff823abd7d5ce0a61b33b6514daf034d28ef074aded29206eaf76', 'STvHoDvOB1Y9znw1ZGl8PiwS+iJ4879QkC72Dt9b3Mk=')")      

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
