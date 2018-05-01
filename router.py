from flask import Flask, render_template, request, url_for, redirect
import subprocess

app = Flask(__name__)

# FOR THE LOVE OF ALL THAT IS HOLY DON'T RUN THIS ON SOMETHING YOU CARE ABOUT

# Debug stuff

def debug(msg):
    print msg

# Global vars
AUTHENTICATED = False
LAN = "255.255.255.255"

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
        debug("Rendering menu..")
        return redirect(url_for('menu'))
    else:
        debug("Must authenticate to proceed")
        message = "You need to login to access the router settings"
        return render_template("index.html", message=message)

@app.route('/menu')
def menu():
    if is_authenticated():
        return render_template("menu.html")
    else:
        return render_template("index.html")

def update_settings(name, lan):
    global LAN
    LAN = lan
    debug("Updated settings: ")
    debug("     LAN: " + LAN + " Name: ")
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
    return render_template("settings.html", message=message, lan=LAN)


@app.route('/ping', methods=["GET", "POST"])
def ping_feature():
    message = ""
    if request.method == "POST":
        data = request.form["address"]
        p = subprocess.Popen('ping -c 3  ' + data, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in p.stdout.readlines():
            message = message + line
    return render_template("ping.html", message=message)
