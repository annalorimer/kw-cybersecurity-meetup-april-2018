from flask import Flask, render_template, request

app = Flask(__name__)

# Global vars
AUTHENTICATED = False

def authenticated():
    return AUTHENTICATED

@app.route('/', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        data = request.form
        if data["username"] == "admin" and data["password"] == "admin":
            print "user/pass is correct"
            AUTHENTICATED = True
            return render_template("settings.html")
    else:
        message = "You need to login to access the router settings"
        return render_template("index.html", message=message)


#@app.route('/settings')
#def settings():
    
