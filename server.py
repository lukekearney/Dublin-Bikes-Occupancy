from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash

import sqlite3, os, json
from src.dbQueries import dbQueries
from src import helpers

path = os.path.dirname(os.path.realpath(__file__))

conn = sqlite3.connect(path + "/bikes.db")

application = Flask(__name__)
    

@application.route("/", methods = ['GET', 'POST'])
def hello():
    db = dbQueries("bikes.db")
    data = db.get_all_names()
    
    #list to string
#     string = str(data)
#     string = string.strip("[]").replace(",", " ")
#     formatted = string.replace("(", "<p>").replace(")", "</p>")
    
    # change list of tuples to list
    formatted = [tuple[0] for tuple in data]
    return render_template("home.html" ,mdata = formatted)


@application.route('/api')
def api():
    return "usage:<br> api/station/STATION_ID/DAY\
    <br>api/static"

    #     db has to be inside function otherwise error about db being created in anohter thread
    db = dbQueries("bikes.db")
    racknum = request.args.get('racknum')
    max_racknum = db.num_bike_stations()
    if int(racknum) > max_racknum:
        # http://flask.pocoo.org/docs/0.10/patterns/errorpages/
        #         return render_template('test.html', mData = data)
        error = "station number out of range. Max is " + (str)(max_racknum)
        return render_template('404.html', mdata=error), 404
    #         return render_template('404.html'), 404
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


@application.route('/api/station/<int:id>')
@application.route('/api/station/<int:id>/<int:day>')
def historical_data(id, day=None):
    """
    gets historical data for a station by id. Used by the client side
    """
    # get all station information by id.
    db = dbQueries("bikes.db")
    max_station = db.num_bike_stations()

    if day is not None:
        if 0 < (int)(id) <= max_station and 0 <= (int)(day) <= 6:
            info = db.get_historical_info_by_id_and_day(id, day)
        else:
            error = "Station must be between 1 and " + (str)(max_station) + ". Day must be between 0 and 6"
            return render_template('404.html', mdata=error), 404
    else:
        if 0 < (int)(id) <= max_station:
            info = db.get_historical_info_by_id(id)
        else:
            error = "Station must be between 0 and " + (str)(max_station)
            return render_template('404.html', mdata=error), 404

    return json.dumps(info)


@application.route("/api/real-time")
def real_time():
    db = dbQueries("bikes.db")
    count = db.get_valid_real_time_count()
    # check if there was valid real_time data
    print(count)
    if count == 0:
        # fetch data from api
        print("no valid data. Fetching new data")
        data = helpers.request_new_data()
        db.insert_new_real_time_values(data)
    # fetch all data to send back
    real_time = db.get_real_time()

    db.close_connection()
    # send results back
    return json.dumps(real_time)


@application.route("/api/real-time/station/<id>")
def real_time_by_station(id):
    db = dbQueries("bikes.db")
    count = db.get_valid_real_time_count()
    # check if there was valid real_time data
    if count == 0:
        # fetch data from api
        data = helpers.request_new_data()
        db.insert_new_real_time_values(data, True)
    # fetch all data to send back
    real_time = db.get_real_time(id)

    # send results back
    return json.dumps(real_time)
    pass


@application.route("/database/setup")
def setup_db():
    db = dbQueries("bikes.db")
    db.setup_db()
    return "setting up database"


@application.route('/to_static_template/<location>')
def to_static_template(location):
    '''
    Used for passing information to the static template
    '''
    database = dbQueries("bikes.db")
    name = location
    id = station_to_ID(name)
    address = station_address_by_ID(id)
    position = station_coordinates_by_ID(id)
    available_bikes = available_bike_stands(id, time)
    available_bike_stands = available_bike_stands(id, time)
    take_credit = take_credit(id)

    return render_template('static-template.html', name=tempName, address=tempAddress,
                           position=tempPosition, available_bikes=availableBikes,
                           available_bike_stands=availableBikeStands)


@application.route('/api/station-info/<name>')
def station(name):
    """
    Gets station information based on the address and loads the appropriate static template
    """
    db = dbQueries("bikes.db")
    # convert name to address
    name = helpers.url_to_name(name)
    info = db.static_info_by_name(name)

    if (len(info) == 0):
        error = "That station does not appear to exist"
        return render_template('404.html', mdata=error), 404

    return json.dumps(info)
@application.route("/station/<address>")
def num_bikes(address):
	db = dbQueries("bikes.db")
	address = address.replace("-", " ")
	id = db.station_to_ID(address)
	count = db.get_valid_real_time_count()
	# check if there was valid real_time data
	if count == 0:
		# fetch data from api
		data = helpers.request_new_data()
		db.insert_new_real_time_values(data, True)
	# fetch all data to send back
	real_time = db.get_real_time(id)
	data = real_time[0]
	return render_template('station.html', Data=data, Address = address)
	

@application.route("/test-station/<address>")
def test_num_bikes(address):
    db = dbQueries("bikes.db")
    address = address.replace("-", " ")
    id = db.station_to_ID(address)
    count = db.get_valid_real_time_count()
    # check if there was valid real_time data
    if count == 0:
        # fetch data from api
        data = helpers.request_new_data()
        db.insert_new_real_time_values(data, True)
    # fetch all data to send back
    real_time = db.get_real_time(id)
    data = real_time[0]
    return render_template('station-test.html', Data=data)


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

    return render_template('test.html', mData=data)


@application.route('/static/test')
def testing():
    return render_template('SpecRunner.html')


if __name__ == "__main__":
    application.debug = True
    application.run(host='0.0.0.0')

# localhost:5000/api?racknum=1
