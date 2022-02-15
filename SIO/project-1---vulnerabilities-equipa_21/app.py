import cherrypy
import sqlite3
import os


SERVER_PATH = os.path.dirname(os.path.abspath(__file__))
DB_STRING = os.path.join(SERVER_PATH, 'database/forum.db')
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
                """%(post_id, title, body, author)
    return info

def get_username():
    return cherrypy.session.get(SESSION_KEY)

def get_correct_button():
    username = get_username()
    if username == None:
        return """<a href="/login" class="btn btn-primary">Login</a>"""
    else:
        return """
                <a href="/profile" class="btn btn-primary">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-person" viewBox="0 0 16 16">
                        <path d="M8 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm2-3a2 2 0 1 1-4 0 2 2 0 0 1 4 0zm4 8c0 1-1 1-1 1H3s-1 0-1-1 1-4 6-4 6 3 6 4zm-1-.004c-.001-.246-.154-.986-.832-1.664C11.516 10.68 10.289 10 8 10c-2.29 0-3.516.68-4.168 1.332-.678.678-.83 1.418-.832 1.664h10z"/>
                    </svg>
                    Profile
                </a>
                <a href="/logout" class="btn btn-primary">Logout</a>
                """

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
            """%(body, author)
    return info
    

class Root(object):
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
                post = conn.execute(f'SELECT (SELECT post_id FROM posts where post_id={id}),title, msg, (SELECT username FROM users WHERE user_id=creator_id) FROM posts WHERE post_id="{id}"')
                com = conn.execute(f'SELECT msg, (SELECT username FROM users WHERE user_id="creator_id") FROM comments WHERE posted_id="{id}"')
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
                res = conn.execute(f'SELECT post_id, title, msg, (SELECT username FROM users WHERE user_id=creator_id) FROM posts WHERE title LIKE "%{name}%"')
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
                res = conn.execute(f'SELECT username, firstname, lastname FROM users WHERE username="{username}"')
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

            return open('./public/profile.html', 'r').read().format("""""", info, message)

    ############################################################################
    # Functions to handle the requests from the client
    @cherrypy.expose
    def add_post(self, title, body):
        author = get_username()
        if author == None:
            raise cherrypy.HTTPRedirect('login')
        else:
            with sqlite3.connect(DB_STRING) as conn:
                conn.execute(f'INSERT INTO posts (title, msg, creator_id) VALUES ("{title}", "{body}", (SELECT user_id FROM users WHERE username="{author}"))')
            raise cherrypy.HTTPRedirect('/')

    @cherrypy.expose
    def add_comment(self, id, body):
        author = get_username()
        if author == None:
            raise cherrypy.HTTPRedirect('login')
        else:
            with sqlite3.connect(DB_STRING) as conn:
                conn.execute(f'INSERT INTO comments (creator_id, posted_id, msg) VALUES ((SELECT user_id FROM users WHERE username="{author}"), "{id}", "{body}")')
            raise cherrypy.HTTPRedirect('/post?id=' + id)
    
    @cherrypy.expose
    def change_password(self, username, new_password, confirm_new_password):
        with sqlite3.connect(DB_STRING) as conn:
            res = conn.execute(f'SELECT 1 FROM users WHERE username="{username}"')

        if res.fetchall() != []:
            if new_password == confirm_new_password:
                with sqlite3.connect(DB_STRING) as conn:
                    conn.execute(f'UPDATE users SET pword="{new_password}" WHERE username="{username}"')

                raise cherrypy.HTTPRedirect('/profile?message=success')
            elif new_password != confirm_new_password:
                raise cherrypy.HTTPRedirect('/profile?message=nomatch')
        else:
            raise cherrypy.HTTPRedirect('/profile?message=nouser')

    @cherrypy.expose
    def register_user(self, username, fname, lname, pw):
        button = """
                <p></p>
                """
        if username == '':
            button = """
                    <p class="text-center" style="color: red">Username can't be empty!</p>
                    """
            return open('./public/register.html').read().format(get_correct_button(), button)

        if fname == '':
            button = """
                    <p class="text-center" style="color: red">First Name can't be empty!</p>
                    """
            return open('./public/register.html').read().format(get_correct_button(), button)

        if lname == '':
            button = """
                    <p class="text-center" style="color: red">Last Name can't be empty!</p>
                    """
            return open('./public/register.html').read().format(get_correct_button(), button)

        if pw == '':
            button = """
                    <p class="text-center" style="color: red">Password can't be empty!</p>
                    """
            return open('./public/register.html').read().format(get_correct_button(), button)

        with sqlite3.connect(DB_STRING) as conn:
            res = conn.execute(f'SELECT 1 FROM users WHERE username="{username}"')
        data = res.fetchall()

        # Check if username already exists
        if data != []:
            button = """
                    <p class="text-center" style="color: red">Username already taken!</p>
                    """
            return open('./public/register.html').read().format(get_correct_button(), button)
        else:
            conn.execute(f'INSERT INTO users (username, firstname, lastname, pword) VALUES ("{username}", "{fname}", "{lname}", "{pw}")')
            conn.commit()
            raise cherrypy.HTTPRedirect('/')
    
    @cherrypy.expose
    def auth(self, username, password):   
        with sqlite3.connect(DB_STRING) as conn:
            # Needs input sanitization
            # Needs password hashing
            res = conn.execute(f'SELECT 1 FROM users WHERE username="{username}" AND pword="{password}"')
        data = res.fetchall()

        # If the user exists, set the session key
        if data == []:
            return open('./public/login.html').read().format("""<p class="text-center" style="color: red">Username or password incorrect!</p>""")
        else:
            cherrypy.session[SESSION_KEY] = cherrypy.request.login = username
            raise cherrypy.HTTPRedirect('/')


if __name__ == '__main__':
    cherrypy.server.socket_port = 8080
    cherrypy.server.socket_host = '127.0.0.1'
    cherrypy.config.update({ 'tools.sessions.on' : True, })
    cherrypy.tree.mount(Root(), "/", conf)
    cherrypy.engine.start()
    cherrypy.engine.block()
