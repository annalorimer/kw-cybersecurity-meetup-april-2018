from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)

# Debug stuff

def debug(msg):
    print msg

# Global vars
AUTHENTICATED = False

def is_authenticated():
    return AUTHENTICATED

def authenticate():
    debug("Authenticated!")
    global AUTHENTICATED 
    AUTHENTICATED = True

def unauthenticate():
    global AUTHENTICATED 
    AUTHENTICATED = False

@app.route('/', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        data = request.form
        # Yeah yeah this is hardcoded sue me I didn't have time to hash and salt it then store it in a db
        if data["username"] == "admin" and data["password"] == "admin":
            authenticate()
    
    if is_authenticated():
        debug("Rendering settings ...")
        return redirect(url_for('settings'))
    else:
        debug("Must authenticate to proceed")
        message = "You need to login to access the router settings"
        return render_template("index.html", message=message)

def update_settings(name, lan):
    return True

@app.route('/settings', methods=["GET", "POST"])
def settings():
    message = ""
    if request.method == "POST":
        data = request.form
        if update_settings(data["name"], data["lan"]):
            message = "Settings updated!"
        else:
            messge = "Error - settings were not updated :("
    return render_template("settings.html", message=message)
