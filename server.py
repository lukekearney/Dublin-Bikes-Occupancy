from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

import src
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
    

if __name__ == "__main__":
    application.debug = True
    application.run(host='localhost')
    
# localhost:5000/api?racknum=1
