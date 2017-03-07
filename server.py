from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash

import sqlite3, os, json
from src.dbQueries import dbQueries
from src import helpers

path = "/var/www/DBApp/bikes.db"

app = Flask(__name__)
    
@app.route("/")
def hello():
    db = dbQueries(path)
    data = db.get_all_names()
    
    # change list of tuples to list
    formatted = [tuple[0] for tuple in data]
    return render_template("home.html" ,mdata = formatted)

@app.route('/api/station-info/<name>')
def station(name):
    """
    Gets station information based on the address and loads the appropriate static template
    """
    db = dbQueries(path)
    # convert name to address
    name = helpers.url_to_name(name)
    info = db.static_info_by_name(name)

    if (len(info) == 0):
        error = "That station does not appear to exist"
        return render_template('404.html', mdata=error), 404

    return json.dumps(info)


@app.route('/api')
def api():
    return "usage:<br> api/station\
    <br> api/static/YOUR_STATION_ID/YOUR_DAY\
    <br> api/real-time\
    <br> api/real-time/station/YOUR_STATION_ID"

    #     db has to be inside function otherwise error about db being created in another thread
    db = dbQueries(path)
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
@app.route('/api/static')
def static_api():
    # open db connection
    conn = sqlite3.connect(path)

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


@app.route('/api/station/<int:id>')
@app.route('/api/station/<int:id>/<int:day>')
def historical_data(id, day=None):
    """
    gets historical data for a station by id. Used by the client side
    """
    # get all station information by id.
    db = dbQueries(path)
    max_station = db.max_station()

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


@app.route("/api/real-time")
def real_time():
    f = open("/tmp/db.log","a")
    f.write("server.py " + path + "\n")
    f.close()
    db = dbQueries(path)
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


@app.route("/api/real-time/station/<id>")
def real_time_by_station(id):
    db = dbQueries(path)
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


@app.route("/database/setup")
def setup_db():
    db = dbQueries(path)
    db.setup_db()
    return "setting up database"


@app.route('/to_static_template/<location>')
def to_static_template(location):
    '''
    Used for passing information to the static template
    '''
    database = dbQueries(path)
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
	

@app.route("/station/<address>")
def test_num_bikes(address):
    db = dbQueries(path)
    
    mdata = db.get_all_names()
    
    # change list of tuples to list
    formatted = [tuple[0] for tuple in mdata]
    
    address = address.replace("-", " ")
    id = db.station_to_ID(address)
    banking = db.take_credit(id)
    if banking == True:
        banking = "Yes"
    else:
        banking = "No"
		
    count = db.get_valid_real_time_count()
    # check if there was valid real_time data
    if count == 0:
        # fetch data from api
        data = helpers.request_new_data()
        db.insert_new_real_time_values(data, True)
    # fetch all data to send back
    real_time = db.get_real_time(id)
    data = real_time[0]
    return render_template('station.html', Data=data, Address = address, mdata = formatted, Banking = banking )

@app.route('/static/test')
def testing():
    return render_template('SpecRunner.html')


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
