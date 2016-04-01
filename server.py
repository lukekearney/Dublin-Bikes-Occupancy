from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

import sqlite3, os, json
import src

path = os.path.dirname(os.path.realpath(__file__))

conn = sqlite3.connect(path + "/bikes.db")

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

# Just adding a route to pull down static data. This can be adjusted later
@application.route('/api/static')
def static_api():
    # open db connection
    conn = sqlite3.connect(path + "/bikes.db")

    c = conn.cursor()
    data = c.execute("SELECT number, name, address, position_lat, position_long, banking FROM static ORDER BY number")
    data = data.fetchall()
    # convert to array of dictionaries
    for i in range(0, len(data)):
        data[i] = {
            "number": data[i][0],
            "name": data[i][1],
            "address": data[i][2],
            "position": {
                "lat": data[i][3],
                "lang": data[i][4]
            },
            "banking": data[i][5] == 'True'
        }

    # close db connection
    conn.close()
    return json.dumps(data)

@application.route('/about')
def about():
    data = [
        {
            "id": 1,
            "name": "Some aname"

        },

        {
            "id": 2,
            "name": "Some aname2"

        },

        {
            "id": 2,
            "name": "Some aname3"

        }
    ]

    return render_template('test.html', mData = data)


if __name__ == "__main__":
    application.debug = True
    application.run(host='0.0.0.0')
    
# localhost:5000/api?racknum=1
