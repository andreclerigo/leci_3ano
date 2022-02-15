import cherrypy
import sqlite3
import os
import hashlib
from base64 import b64encode, b64decode
from encrypt_db import encrypt
from decrypt_db import decrypt
import json
from echap import peer


SERVER_PATH = os.path.dirname(os.path.abspath(__file__))
DB_DIRECTORY = os.path.join(SERVER_PATH, 'database/')
DB_STRING = os.path.join(DB_DIRECTORY, 'uap.db')
SUPPORTED_PROTOCOLS = ['E-CHAP']

conf = {
    "/": { 'tools.staticdir.root': SERVER_PATH, },
    "/public": { "tools.staticdir.on": True,
			    "tools.staticdir.dir": "public" },
    "/public/css": { "tools.staticdir.on": True,
			        "tools.staticdir.dir": "public/css" },
    "/public/js": { "tools.staticdir.on": True,
			        "tools.staticdir.dir": "public/js" },
}

# Returns the sanitized text
def sanitize_input(text):
    if '<' in text:
        text = text.replace('<','&lt;')
    elif '>' in text:
        text = text.replace('>','&gt;')   
    return text

def get_username():
    return cherrypy.session.get('username')

def get_password():
    return cherrypy.session.get('password')

def get_vault():
    return cherrypy.session.get('vault')

def get_referer():
    return cherrypy.session.get('referer')

# Returns the dictionary of credentials
def decrypt_json(username):
    json_path = os.path.join(DB_DIRECTORY, username+'.json')
    with open(json_path, 'rb') as f:
        nonce = f.read(16)
        salt = f.read(32)
        signature = f.read(32)
        data = f.read()
    
    decrypted_data = decrypt(data, get_password(), nonce, salt, signature)

    return json.loads(decrypted_data)    

# Returns the HTML card associated with the credentials
def get_credentials():
    vault = get_vault()
    info = ""
    for dns in vault:
        for credentials in vault[dns]:          
            info += """ 
                    <div class="card center bg-light" style="width: 40rem"">
                        <div class="card-body">
                            <h5 class="card-title text-center">Service: %s</h5>
                            <p class="card-text text-center">Username: %s</p>
                            <p class="card-text text-center">
                                Password: <span id="%s" class="hiddenText">%s</span>
                                <button class="btn btn-transparent btn-sm shadow-none" id="%s" onclick="reply_click(this.id)">
                                    <i class="bi bi-eye-slash-fill"></i>
                                </button>
                            </p>
                            <p class="card-text text-right">
                                <a href="/delete_credential?dns=%s&username=%s">
                                <button class="btn btn-danger">
                                    <i class="bi bi-x-circle"></i>
                                    Delete
                                </button>
                                </a>
                            </p>  
                        </div>                                                     
                    </div>
                    """ % (dns, credentials['username'], dns+'_'+credentials['username'], credentials['password'],
                        dns+'_'+credentials['username'], dns, credentials['username'])
    return info

# Returns the HTML card associated with the credentials for a specific dns
def get_dns_credentials(dns_name):
    count = 0
    vault = get_vault()
    info = ""
    for dns in vault:
        if dns == dns_name:
            for credentials in vault[dns]:  
                info += """ <a class="dropdown-item text-center" href="/auth?username=%s&password=%s&selected_acc=%i"> 
                        <div class="card center bg-dark text-center" style="width: 20rem">
                            <div class="card-body text-center bg-light">
                                <h5 class="card-title text-center">Service: %s</h5>
                                <p class="card-text text-center">Username: %s</p> 
                            </div>                                                     
                        </div> </a>
                        """ % (get_username(), get_password(), count, dns, credentials['username'])
                count += 1
    return info

class Root(object):
    # Error Handling Page for 404, 500, ...
    _cp_config = {
        'error_page.default': os.path.join(SERVER_PATH, "public/error.html")
    }

    # Functions to serve the html pages
    @cherrypy.expose
    def index(self, msg_dns=None, msg_pw=None):
        username = get_username()

        if username == None:
            raise cherrypy.HTTPRedirect('/login')
        else:
            if msg_dns == None:
                msg_dns = """<p></p>"""
            elif msg_dns == 'success':
                msg_dns = """<p class="text-center" style="color: green"><b>Domain successfully added!</b></p>"""
            elif msg_dns == 'repeat':
                msg_dns = """<p class="text-center" style="color: red"><b>Domain already registered!</b></p>"""
            elif msg_dns == 'error':
                msg_dns = """<p class="text-center" style="color: red"><b>Credentials must have characters!</b></p>"""
            elif msg_dns == 'error_ur':
                msg_dns = """<p class="text-center" style="color: red"><b>Username already exists in that DNS!</b></p>"""


            if msg_pw == None:
                msg_pw = """<p></p>"""
            elif msg_pw == 'success':
                msg_pw = """<p class="text-center" style="color: green"><b>Password changed successfully!</b></p>"""
            elif msg_pw == 'nouser':
                msg_pw = """<p class="text-center" style="color: red"><b>User not found!</b></p>"""
            elif msg_pw == 'nomatch':
                msg_pw = """<p class="text-center" style="color: red"><b>Passwords don't match!</b></p>"""
            elif msg_pw == 'oldnomatch':
                msg_pw = """<p class="text-center" style="color: red"<b>Wrong current password!</b></p>"""
            elif msg_pw == 'badformat':
                msg_pw = """<p class="text-center" style="color: red"<b>Password must only contain numbers and letters!</b></p>"""
            
            return open('./public/index.html', 'r').read().format(msg_dns, msg_pw, get_credentials())

    @cherrypy.expose
    def login(self, protocol=None):
        # Check which service called /login
        referer = None
        if 'Referer' in cherrypy.request.headers:
            referer = cherrypy.request.headers['Referer']
            if referer.startswith('http://'):
                referer = referer[7:]
            referer = referer.split('/')[0]

        cherrypy.session['referer'] = referer

        # If no Referer, redirect to a normal login
        if referer == None or referer == 'localhost:8081' or referer == '127.0.0.1:8081':
            return open('./public/login.html', 'r').read().format("""<p></p>""", """<p></p>""")

        # If there is a Referer and no protocol is mentioned, use E-CHAP
        if protocol == None:
            protocol='E-CHAP'
        else:
            protocol = protocol.upper()
            
            # If the protocol is not supported, show an error page
            if protocol not in SUPPORTED_PROTOCOLS:
                return open('./public/no_credential.html').read().format(f"""{protocol} protocol is not supported""")
        
        cherrypy.session['protocol'] = protocol
        return open('./public/login.html', 'r').read().format("""<p></p>""", f"""Using {protocol} protocol to authenticate {referer}""")

    @cherrypy.expose
    def register(self):
        return open('./public/register.html').read().format("""<p></p>""")

    @cherrypy.expose
    def logout(self):
        cherrypy.session['username'] = None
        cherrypy.session['password'] = None
        cherrypy.session['vault'] = None
        cherrypy.session['protocol'] = None
        raise cherrypy.HTTPRedirect('/')

    ############################################################################
    # Functions to handle the requests from the client

    @cherrypy.expose
    def delete_credential(self, dns, username):
        vault = get_vault()

        # Remove only credentials in DNS
        vault[dns] = [vault[dns][ind] for ind, x in enumerate(vault[dns]) 
                if vault[dns][ind]['username'] != username]
        
        # If DNS is empty remove DNS
        if(vault[dns] == []):
            vault.pop(dns, None)

        cherrypy.session['vault'] = vault        

        # Convert credentials to JSON object
        data = json.dumps(vault, indent = 4)
        encrypted_data, nonce, salt, signature = encrypt(data.encode(), get_password())

        # Create encrypted file
        with open(os.path.join(DB_DIRECTORY, get_username()+'.json'), 'wb') as f:
            f.write(nonce)
            f.write(salt)
            f.write(signature)
            f.write(encrypted_data)
        
        raise cherrypy.HTTPRedirect('/')

    @cherrypy.expose
    def add_credential(self, dns, username, password):
        vault = get_vault()
        
        if dns == "" or username == "" or password == "":
            raise cherrypy.HTTPRedirect('/?msg_dns=error')

        # cannot have repeated usernames for same DNS
        if dns in vault:
            for cred in vault[dns]:
                if cred['username'] == username:
                    raise cherrypy.HTTPRedirect('/?msg_dns=error_ur')

        if dns not in vault:
            vault[dns] = [{ 'username': username, 'password': password }]
        else:
            vault[dns].append({ 'username': username, 'password': password })

        cherrypy.session['vault'] = vault

        data = json.dumps(vault, indent = 4)
        encrypted_data, nonce, salt, signature = encrypt(data.encode(), get_password())

        # Create encrypted file
        with open(os.path.join(DB_DIRECTORY, get_username()+'.json'), 'wb') as f:
            f.write(nonce)
            f.write(salt)
            f.write(signature)
            f.write(encrypted_data)

        raise cherrypy.HTTPRedirect('/?msg_dns=success')
        
    @cherrypy.expose
    def change_password(self, username, current_password, new_password, confirm_new_password):
        if not username.isalnum():
            raise cherrypy.HTTPRedirect('/?msg_pw=nouser')

        with sqlite3.connect(DB_STRING) as conn:
            res = conn.execute('SELECT pword, salt FROM users WHERE username="%s"' % username)
        data = res.fetchall()

        if data != []:
            # Use the salt on the database to hash the new password
            salt = b64decode(data[0][1])

            if data[0][0] != hashlib.sha256(current_password.encode() +  salt).hexdigest():
                raise cherrypy.HTTPRedirect('/?msg_pw=oldnomatch')
            elif new_password == confirm_new_password:
                if not new_password.isalnum():
                    raise cherrypy.HTTPRedirect('/?msg_pw=badformat')
                
                # Create the new hashed password
                hashed_new_password = hashlib.sha256(new_password.encode() + salt).hexdigest()

                cherrypy.session['password'] = new_password

                # Create a new credential vault empty and encrypt it
                data = json.dumps(get_vault(), indent = 4)
                encrypted_data, nonce, salt, signature = encrypt(data.encode(), new_password)

                # Create encrypted file
                with open(os.path.join(DB_DIRECTORY, username+'.json'), 'wb') as f:
                    f.write(nonce)
                    f.write(salt)
                    f.write(signature)
                    f.write(encrypted_data)

                with sqlite3.connect(DB_STRING) as conn:
                    conn.execute('UPDATE users SET pword="%s" WHERE username="%s"' % (hashed_new_password, username))
                raise cherrypy.HTTPRedirect('/?msg_pw=success')
            
            elif new_password != confirm_new_password:
                raise cherrypy.HTTPRedirect('/?msg_pw=nomatch')
        else:
            raise cherrypy.HTTPRedirect('/?msg_pw=nouser')

    @cherrypy.expose
    def register_user(self, username, pw):
        if not username.isalnum():
            button = """<p class="text-center" style="color: red">Username can only contain numbers and letters!</p>"""
            return open('./public/register.html').read().format(button)

        if not pw.isalnum():
            button = """<p class="text-center" style="color: red">Password can only contain numbers and letters!</p>"""
            return open('./public/register.html').read().format(button)
        
        # Associate the username with an hashed password and random salt used to hash the password
        salt = os.urandom(32)
        salt_e = b64encode(salt).decode('utf-8')
        hashed_pw = hashlib.sha256(pw.encode() + salt).hexdigest()

        with sqlite3.connect(DB_STRING) as conn:
            res = conn.execute('SELECT * FROM users WHERE username="%s"' % username)
        data = res.fetchall()

        # Check if username already exists
        if data != []:
            button = """<p class="text-center" style="color: red">Username already taken!</p>"""
            return open('./public/register.html').read().format(button)
        else:
            file_path = os.path.join(DB_DIRECTORY, username + '.json')
            conn.execute('INSERT INTO users (username, pword, salt, file_path) VALUES ("%s", "%s", "%s", "%s")' % (username, hashed_pw, salt_e, username+'.json'))
            conn.commit()

            # Create JSON file
            data = json.dumps({}, indent = 4)
            encrypted_data, nonce, salt, signature = encrypt(data.encode(), pw)

            # Create encrypted file
            with open(file_path, 'wb') as f:
                f.write(nonce)
                f.write(salt)
                f.write(signature)
                f.write(encrypted_data)

            raise cherrypy.HTTPRedirect('/')
    
    @cherrypy.expose
    def auth(self, username, password, selected_acc=None):
        if not username.isalnum() or not password.isalnum():
            return open('./public/login.html').read().format("""<p class="text-center" style="color: red">Username or password incorrect!</p>""", """<p></p>""")
        
        with sqlite3.connect(DB_STRING) as conn:
            res = conn.execute('SELECT * FROM users WHERE username="%s"' % username)
        data = res.fetchall()

        # If the user exists, set the session key
        if data == []:
            return open('./public/login.html').read().format("""<p class="text-center" style="color: red">Username or password incorrect!</p>""", """<p></p>""")
        else:
            # Use the salt to check if hashes match
            salt = b64decode(data[0][3])
            hashed_password = hashlib.sha256(password.encode() + salt).hexdigest()

            if hashed_password != data[0][2]:
                return open('./public/login.html').read().format("""<p class="text-center" style="color: red">Username or password incorrect!</p>""", """<p></p>""")

            cherrypy.session['username'] = username
            cherrypy.session['password'] = password
            cherrypy.session['vault'] = decrypt_json(username)

            # Check if referer is set
            referer = get_referer()
            
            # Redirect to the referer website if it exists
            if referer != None and referer != 'localhost:8081' and referer != '127.0.0.1:8081':
                if referer not in get_vault():
                    return open('./public/no_credential.html').read().format(f"""{username} has no credential for {referer}""")
                  
                vault = get_vault()

                # Select the correct account
                html_string = get_dns_credentials(referer)

                # If only one account is available, select it
                if len(vault[referer]) == 1:
                    credential = vault[referer][0]
                else:
                    # If no account selected, make the user choose it
                    if selected_acc == None:
                        return open('./public/choose_credential.html').read().format(html_string)
                    
                    # Find the correct credential
                    credential = vault[referer][int(selected_acc)]

                if cherrypy.session.get('protocol') == 'E-CHAP':
                    code, token = peer(credential['username'], credential['password'])

                # If the peer request fail, redirect to an error page
                if code == False:
                    return open('./public/no_credential.html').read().format(f"""Authentication failed! Verificantion failed on bit {token}""")
                
                # If the peer request was successfull, redirect to the referer website
                cherrypy.session['referer'] = None
                cherrypy.session['protocol'] = None
                raise cherrypy.HTTPRedirect(f"http://{referer}/auth?token={token}")
            raise cherrypy.HTTPRedirect('/')

if __name__ == '__main__':
    cherrypy.server.socket_port = 8081
    cherrypy.server.socket_host = '127.0.0.1'
    cherrypy.config.update({ 'tools.sessions.on' : True, })
    cherrypy.tree.mount(Root(), "/", conf)
    cherrypy.engine.start()
    cherrypy.engine.block()
