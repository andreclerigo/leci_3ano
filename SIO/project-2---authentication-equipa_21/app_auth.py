import cherrypy
import sqlite3
import os
import hashlib
from base64 import b64encode, b64decode
from uap.echap import authenticator


SERVER_PATH = os.path.dirname(os.path.abspath(__file__))
DB_STRING = os.path.join(SERVER_PATH, 'database/forum_sec.db')
SESSION_KEY = 'FORUM_KEY'

conf = {
    "/": { 'tools.staticdir.root': SERVER_PATH, },
    "/public": { "tools.staticdir.on": True,
			    "tools.staticdir.dir": "public" },
    "/public/css": { "tools.staticdir.on": True,
			        "tools.staticdir.dir": "public/css" },
    "/public/js": { "tools.staticdir.on": True,
			        "tools.staticdir.dir": "public/js" },
}

# Returns the HTML card for the posts in the website
def get_posts_info(data):
    info = ''
    for row in data:
        post_id = row[0]
        title = row[1]
        body = row[2].replace('\\n', '<br>')
        author = row[3]
        info += """
                <a href="/post?id=%i" class="a-hidden">
                    <div class="card center" style="width: 80rem">
                        <div class="card-body">
                            <h5 class="card-title text-center">%s</h5>
                            <p class="card-text text-center">%s</p>
                            <p class="card-text text-right">%s</p>                  
                        </div>                                                     
                    </div>
                </a> 
                """%(post_id, sanitize_input(title), sanitize_input(body), author)
    return info

# Returns the sanitized text
def sanitize_input(text):
    if '<' in text:
        text = text.replace('<','&lt;')
    elif '>' in text:
        text = text.replace('>','&gt;')   
    return text

def get_username():
    return cherrypy.session.get(SESSION_KEY)

# Returns either Login buttons or the logout button
def get_correct_button():
    username = get_username()
    if username == None:
        return """
                <div class="col-" style="margin-right: 20px;">
                    <a href="/login" class="btn btn-primary">Login</a>
                </div>
                <div class="col-">
                    <a href="http://localhost:8081/login?protocol=e-chap">
                    <button type="button" class="btn btn-primary">
                        <i class="bi bi-key"></i>
                        Secure Login
                    </button>
                    </a>
                </div>
                """
    else:
        return """
                <div class="col-" style="margin-right: 20px;">
                    <a href="/profile" class="btn btn-primary">
                        <i class="bi bi-person"></i>
                        Profile
                    </a>
                    <a href="/logout" class="btn btn-primary">Logout</a>
                </div>
                """

# Returns the HTML for the comment section
def getCom(post, com):
    postData = post.fetchall()
    comData = com.fetchall()
    info = get_posts_info(postData)
    
    for row in comData:
        body = row[0].replace('\\n', '<br>')
        author = row[1]
        info += """
            <div class="card center" style="width: 50rem">
                <div class="card-body">
                    <p class="card-text text-center">%s</p>
                    <p class="card-text text-right">%s</p>                  
                </div>                                                     
            </div>
            """%(sanitize_input(body), sanitize_input(author))
    return info


class Root(object):
    # Error Handling Page for 404, 500, ...
    _cp_config = {
        'error_page.default': os.path.join(SERVER_PATH, "./public/error.html")
    }

    # Functions to serve the html pages
    @cherrypy.expose
    def index(self):
        with sqlite3.connect(DB_STRING) as conn:
            res = conn.execute('SELECT post_id, title, msg, (SELECT username FROM users WHERE user_id=creator_id) FROM posts')
        
        data = res.fetchall()
        return open('./public/index.html', 'r').read().format(get_correct_button(), get_posts_info(data))

    @cherrypy.expose
    def login(self):
        return open('./public/login.html', 'r').read().format("""<p></p>""")

    @cherrypy.expose 
    def post(self, id):
        if id == '':
            raise cherrypy.HTTPRedirect('/')
        else:
            with sqlite3.connect(DB_STRING) as conn:
                post = conn.execute('SELECT (SELECT post_id FROM posts where post_id=%i), title, msg, (SELECT username FROM users WHERE user_id=creator_id) FROM posts WHERE post_id=%i' % (int(id), int(id)))
                com = conn.execute('SELECT msg, (SELECT username FROM users WHERE user_id="creator_id") FROM comments WHERE posted_id=%i' % int(id))
            return open('./public/post.html', 'r').read().format(get_correct_button(), id, getCom(post, com))

    @cherrypy.expose
    def register(self):
        return open('./public/register.html').read().format(get_correct_button(), """<p></p>""")

    @cherrypy.expose
    def search(self, name):
        if name == '':
            raise cherrypy.HTTPRedirect('/')
        else:
            with sqlite3.connect(DB_STRING) as conn:
                res = conn.execute('SELECT post_id, title, msg, (SELECT username FROM users WHERE user_id=creator_id) FROM posts WHERE title LIKE "%s"' % ("%" + name.replace("\"", "'") + "%"))
            return open('./public/index.html', 'r').read().format(get_correct_button(), get_posts_info(res))

    @cherrypy.expose
    def logout(self):
        cherrypy.session[SESSION_KEY] = cherrypy.request.login = None
        raise cherrypy.HTTPRedirect('/')
    
    @cherrypy.expose
    def profile(self, message=None):
        username = get_username()

        if username == None:
            raise cherrypy.HTTPRedirect('/login')
        else:
            with sqlite3.connect(DB_STRING) as conn:
                res = conn.execute('SELECT username, firstname, lastname FROM users WHERE username="%s"' % username)
            data = res.fetchall()

            info = ''
            for row in data:
                user = row[0]
                fname = row[1]
                lname = row[2].replace('\\n', '<br>')
                info += """
                        <div class="text-light text-center" style="margin-top: 20vh">
                            <h1>Username: %s</h1>
                            <h1>First Name: %s</h1>
                            <h1>Last Name: %s</h1>
                        </div>
                        """%(user, fname, lname)

            if message == None:
                message = """<p></p>"""
            elif message == 'success':
                message = """<p class="text-center" style="color: green"><b>Password changed successfully!</b></p>"""
            elif message == 'nouser':
                message = """<p class="text-center" style="color: red"><b>User not found!</b></p>"""
            elif message == 'nomatch':
                message = """<p class="text-center" style="color: red"><b>Passwords don't match!</b></p>"""
            elif message == 'oldnomatch':
                message = """<p class="text-center" style="color: red"<b>Wrong current password!</b></p>"""
            elif message == 'badformat':
                message = """<p class="text-center" style="color: red"<b>Password must only contain numbers and letters!</b></p>"""

            old_password = """<div class="form-group">
                                <label for="recipient-name" class="col-form-label">Current Password</label>
                                <input type="password" class="form-control" name="current_password" id="current_password">
                            </div>"""

            return open('./public/profile.html', 'r').read().format(old_password, info, message)

    ############################################################################
    # Functions to handle the requests from the client
    @cherrypy.expose
    def add_post(self, title, body):
        author = get_username()
        if author == None:
            raise cherrypy.HTTPRedirect('login')
        else:
            with sqlite3.connect(DB_STRING) as conn:
                conn.execute('INSERT INTO posts (title, msg, creator_id) VALUES ("%s", "%s", (SELECT user_id FROM users WHERE username="%s"))' % (title.replace("\"", "'"), body.replace("\"", "'"), author))
            raise cherrypy.HTTPRedirect('/')

    @cherrypy.expose
    def add_comment(self, id, body):
        author = get_username()
        if author == None:
            raise cherrypy.HTTPRedirect('login')
        else:
            with sqlite3.connect(DB_STRING) as conn:
                conn.execute('INSERT INTO comments (creator_id, posted_id, msg) VALUES ((SELECT user_id FROM users WHERE username="%s"), %i, "%s")' % (author, int(id), body.replace("\"", "'")))
            raise cherrypy.HTTPRedirect('/post?id='+id)
    
    @cherrypy.expose
    def change_password(self, username, current_password, new_password, confirm_new_password):
        if not username.isalnum():
            raise cherrypy.HTTPRedirect('/profile?message=nouser')

        with sqlite3.connect(DB_STRING) as conn:
            res = conn.execute('SELECT pword, salt FROM users WHERE username="%s"' % username)
        data = res.fetchall()

        if data != []:
            # Use the salt on the database to hash the new password
            salt = b64decode(data[0][1])

            if data[0][0] != hashlib.sha256(current_password.encode() +  salt).hexdigest():
                raise cherrypy.HTTPRedirect('/profile?message=oldnomatch')
            elif new_password == confirm_new_password:
                if not new_password.isalnum():
                    raise cherrypy.HTTPRedirect('/profile?message=badformat')
                
                # Create the new hashed password
                hashed_new_password = hashlib.sha256(new_password.encode() + salt).hexdigest()

                with sqlite3.connect(DB_STRING) as conn:
                    conn.execute('UPDATE users SET pword="%s" WHERE username="%s"' % (hashed_new_password, username))
                raise cherrypy.HTTPRedirect('/profile?message=success')
            
            elif new_password != confirm_new_password:
                raise cherrypy.HTTPRedirect('/profile?message=nomatch')
        else:
            raise cherrypy.HTTPRedirect('/profile?message=nouser')

    @cherrypy.expose
    def register_user(self, username, fname, lname, pw):
        if not username.isalnum():
            button = """<p class="text-center" style="color: red">Username can only contain numbers and letters!</p>"""
            return open('./public/register.html').read().format(get_correct_button(), button)

        if not fname.isalnum():
            button = """<p class="text-center" style="color: red">First Name can only contain numbers and letters!</p>"""
            return open('./public/register.html').read().format(get_correct_button(), button)

        if not lname.isalnum():
            button = """<p class="text-center" style="color: red">Last Name can only contain numbers and letters!</p>"""
            return open('./public/register.html').read().format(get_correct_button(), button)

        if not pw.isalnum():
            button = """<p class="text-center" style="color: red">Password can only contain numbers and letters!</p>"""
            return open('./public/register.html').read().format(get_correct_button(), button)
        
        # Associate the username with an hashed password and random salt used to hash the password
        salt = os.urandom(32)
        salt_e = b64encode(salt).decode('utf-8')
        pw = hashlib.sha256(pw.encode() + salt).hexdigest()

        with sqlite3.connect(DB_STRING) as conn:
            res = conn.execute('SELECT * FROM users WHERE username="%s"' % username)
        data = res.fetchall()

        # Check if username already exists
        if data != []:
            button = """<p class="text-center" style="color: red">Username already taken!</p>"""
            return open('./public/register.html').read().format(get_correct_button(), button)
        else:
            conn.execute('INSERT INTO users (username, firstname, lastname, pword, salt) VALUES ("%s", "%s", "%s", "%s", "%s")' % (username, fname.replace("\"", "'"), lname.replace("\"", "'"), pw, salt_e))
            conn.commit()
            raise cherrypy.HTTPRedirect('/')
    
    @cherrypy.expose
    def auth(self, username=None, password=None, token=None):
        if token != None:
            with sqlite3.connect(DB_STRING) as conn:
                res = conn.execute('SELECT * FROM users WHERE auth_token="%s"' % token.replace("\"", "'"))
            data = res.fetchall()

            # Check if auth token exists
            if data != []:
                # Rewrite token to NULL
                with sqlite3.connect(DB_STRING) as conn:
                    conn.execute('UPDATE users SET auth_token=NULL WHERE auth_token="%s"' % token.replace("\"", "'"))
                    conn.commit()
                
                cherrypy.session[SESSION_KEY] = cherrypy.request.login = data[0][1]
            raise cherrypy.HTTPRedirect('/')

        # Check if username and password are valid
        if username == None or password == None or not username.isalnum() or not password.isalnum():
            return open('./public/login.html').read().format("""<p class="text-center" style="color: red">Username or password incorrect!</p>""")
        
        with sqlite3.connect(DB_STRING) as conn:
            res = conn.execute('SELECT * FROM users WHERE username="%s"' % username)
        data = res.fetchall()

        # If the user exists, set the session key
        if data == []:
            return open('./public/login.html').read().format("""<p class="text-center" style="color: red">Username or password incorrect!</p>""")
        else:
            # Use the salt to check if hashes match
            salt = b64decode(data[0][5])
            password = hashlib.sha256(password.encode() + salt).hexdigest()

            if password != data[0][4]:
                return open('./public/login.html').read().format("""<p class="text-center" style="color: red">Username or password incorrect!</p>""")

            cherrypy.session[SESSION_KEY] = cherrypy.request.login = username
            raise cherrypy.HTTPRedirect('/')


if __name__ == '__main__':
    cherrypy.server.socket_port = 8080
    cherrypy.server.socket_host = '127.0.0.1'
    cherrypy.config.update({ 'tools.sessions.on' : True, })
    cherrypy.tree.mount(Root(), "/", conf)
    cherrypy.engine.start()
    authenticator(DB_STRING)
