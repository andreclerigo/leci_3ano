## Description
Our project implements a simple Forum website which displays all posts in the front page by chronological order (oldest first), the user can use the search bar to search for a specific post by title. Within this Forum it is possible to create new users, login while maintaining a session, that is, while the server is running, it is enough to log in once for the site to recognize the user who is accessing it. It is also possible to create posts with title, content and author, where the title and content are enabled by the user, but the author field is automatically filled in by the backend using a session.<br>
In the same way, the comments also have content and author, and the author field is also filled in automatically.<br>
It should be noted that when the user is not logged in, he is redirected to an authentication page when he tries to make a post or comment.

## Vulnerabilites used
[CWE-79](https://cwe.mitre.org/data/definitions/79.html)

[CWE-89](https://cwe.mitre.org/data/definitions/89.html)

[CWE-256](https://cwe.mitre.org/data/definitions/256.html)

[CWE-620](https://cwe.mitre.org/data/definitions/620.html)

[CWE-756](https://cwe.mitre.org/data/definitions/756.html)

## How to run
1. Create a virtual enviorment:
```bash
python3 -m venv venv
```

2. Activate the virtual enviorment (you will need to repeast this step every time you open a new terminal):
```bash
source venv/bin/activate
```

3. Install the requeriments:
```bash
pip install -r requirements.txt
```

4. Run the server:
```bash
python3 app.py
```
or 
```bash
python3 app_sec.py
```

5. Access the website:

http://127.0.0.1:8080/


## Authors
André Clérigo, 98485

Cláudio Asensio, 98433

Hugo Domingos, 98502

Tiago Marques, 98459
