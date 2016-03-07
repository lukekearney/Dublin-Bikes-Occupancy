from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

import src
application = Flask(__name__)

@application.route("/")
def hello():
    return render_template("home.html")

# Add whatever api route you want here
@application.route("/api")
def api():
    return "api"

if __name__ == "__main__":
    application.run(host='0.0.0.0')
