from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

import sqlite3, os
import src

path = os.path.dirname(os.path.realpath(__file__))
conn = sqlite3.connect(path + "/bikes.db")

c = conn.cursor()
application = Flask(__name__)

@application.route("/")
def hello():
    return render_template("home.html")

# Add whatever api route you want here
@application.route('/api')
def api():
#     racknum = request.args.get('racknum')
#     return racknum

    racknum = request.args.get('racknum')
    max_racknum = 10
    if int(racknum) > max_racknum:
        # http://flask.pocoo.org/docs/0.10/patterns/errorpages/
        return render_template('404.html'), 404
    else:
        return racknum

# Add whatever api route you want here
@application.route('/api/static')
def static_api():


    
    

if __name__ == "__main__":
    application.debug = True
    application.run(host='0.0.0.0')
    
# localhost:5000/api?racknum=1
