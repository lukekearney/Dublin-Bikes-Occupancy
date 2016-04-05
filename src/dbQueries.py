__author__ = "Ellen Rushe"

import sqlite3
import time
import datetime

class dbQueries:
    
    def __init__(self, database_name):
        '''Connect to database[1]'''
        self.conn = sqlite3.connect(database_name)

    def label_results(self, keys, results):
        '''
        Parameter(s): a list of keys and a list of results
        Returns: a dictionary labelled with the appropriate keys and values
        '''
        returned_results = {}


        for index, item in enumerate(results):
            print(item)
            returned_results[keys[index]] = item

        return returned_results


    def setup_db(self):
        """
        Initialises the database
        """
        query = self.conn.execute('CREATE TABLE IF NOT EXISTS real_time (number int, bike_stands int, '
                                  'available_bikes int, available_bike_stands int, status text, '
                                  'updated int)')

    def exists(self, number, table):
        '''
        Parameter(s): the number of the station and the table to search in
        Returns: a boolean for whether the item exists in the table or not
        '''
        c = self.conn.cursor()
        query = self.QueryBuilder().count(["number"], table).where([[
            "number", "=", number
        ]]).getQuery()
        print(query)
        c.execute(query["sql"], query["values"])

        results = c.execute(query["sql"], query["values"]).fetchall()[0][0]


        if results > 0:
            return True
        else:
            return False


    class QueryBuilder:
        def __init__(self):
            self.query = "";
            self.values = []

        def select(self, fields, table):
            '''
            Parameter(s): a list of fields and a table in the database
            Returns: the current object with the query built up
            '''
            query = "SELECT "
            for index, field in enumerate(fields):
                query += field
                if index < len(fields) - 1:
                    query += ","

            self.query = query + " FROM " + table

            return self

        def count(self, fields, table):
            '''
            Parameter(s): a list of fields and a table in the database
            Returns: a query to count the number of results
            '''
            query = "SELECT COUNT("

            for index, field in enumerate(fields):
                query += field
                if index < len(fields) - 1:
                    query += ","

            self.query = query + ") FROM " + table
            return self

        def insert(self, fields, values, table):
            query = "INSERT INTO " + table
            field_string = ""
            value_string = ""
            if fields:
                field_string += " ("
                for index, field in enumerate(fields):
                    field_string += field
                    if index < len(fields) - 1:
                        field_string += ","

                field_string += ")"

            query += field_string + " VALUES "

            print(values)
            if type(values[0]) is list or type(values[0]) is tuple:
                # has multiple rows to

                for index, value in enumerate(values):
                    for val in value:
                        self.values.append(val)

                    value_string += "(" + ",".join("?" for x in value) + ")"
                    if index < len(values) - 1:
                        value_string += ","

            else:
                # has only 1 value to insert
                values = [val for val in values]
                value_string += "(" + ",".join("?" for x in values) + ")"

            # set the value of the query
            self.query = query + value_string

            return self

        def join(self, table, table1col, table2col):
            query = " JOIN " + table + " ON " + table1col + " = " + table2col
            print(query)
            self.query += query
            return self

        def update(self, fields, values, table):
            query = "UPDATE " + table + " SET "
            for index, key in enumerate(fields):
                query += key + "=?"
                self.values.append(values[index])
                if index < len(fields) - 1:
                    query += ","

            self.query = query
            return self


        def where(self, parameters):
            '''
            Parameter(s): a list of fields and a table in the database. Parameters in formation [field, action, value]
            Returns: the current object with the query built up
            '''
            query = ""
            for index, param in enumerate(parameters):
                query += param[0] + " " + param[1] + "?"
                self.values.append(param[2])

                if index < len(parameters) - 1:
                    query += " AND "

            self.query += " WHERE " + query
            return self

        def groupBy(self, field):
            self.query += " GROUP BY " + field
            return self

        def getQuery(self):
            return {
                "sql" : self.query,
                "values" : self.values
            }




        
    def station_to_ID(self, name):
        '''
        Parameter(s): Name of station (string).
        Returns: Number of station based on the name of the station.
        '''
        # If name is entered in lowercase or otherwise it will be converted to uppercase. 
        name = name.upper()
        # Retrieves number of station based on the name of the station [2].
        query = self.conn.execute('SELECT number FROM static WHERE name = :name', {'name':name})
        for row in query:
            return row[0]
        
    def station_address_by_name(self, name): 
        '''
        Parameter(s): Name of station (string).
        Returns: Address of station based on the name of the station.
        ''' 
        # Retrieves address of station based on the name of the station [2].
        query = self.conn.execute('SELECT address FROM static WHERE name = :name', {'name':name})
        for row in query:
            return row[0]
        
    def station_address_by_ID(self, number):
        '''
        Parameter(s): Number of station (string).
        Returns: Address of station based on the ID of the station.
        ''' 
        # Retrieves address of station based on the number (i.e. the ID) of the station [2].
        query = self.conn.execute('SELECT address FROM static WHERE number = :number', {'number':number})
        for row in query:
            return row[0]
        
    def station_coordinates_by_name(self, name):
        '''
        Parameter(s): Name of station (string).
        Returns: Co-ordinates of station based on the name of the station.
        ''' 
        # Retrieves co-ordinates of station based on the name of the station [2].
        query = self.conn.execute('SELECT position_long, position_lat FROM static WHERE name = :name', {'name':name})
        for row in query:
            return row
        
    def station_coordinates_by_ID (self, number):
        '''
        Parameter(s): Number of station (string).
        Returns: Co-ordinates of station based on the ID of the station.
        ''' 
        # Retrieves co-ordinates of station based on the number (i.e. the ID) of the station [2].
        query = self.conn.execute('SELECT position_long, position_lat FROM static WHERE number = :number', {'number':number})
        for row in query:
            return row

    def static_info_by_name (self, name):
        name = name.upper()
        keys = ["number", "name", "address"]
        query = self.QueryBuilder().select(keys, "static").where([
            ["name", "=", name]
        ]).getQuery()
        print(query)
        c = self.conn.cursor()

        c.execute(query["sql"], query["values"])
        items = c.fetchall()

        # labels each result
        grouped_items = [self.label_results(keys, item) for item in items]

        return grouped_items



    def available_bike_stands(self, number, time):
        '''
        Parameter(s): ID of station, logged time (strings).
        Returns: Available bikes stands based on station ID and logged time specified. 
        ''' 
        # Retrieves available bikes stands based on the number of the station and the time(epoch time)[2]. 
        query = self.conn.execute('SELECT available_bike_stands FROM dynamic WHERE number = :number AND logged = :time ', {'number':number, 'time':time})
        for row in query:
            return row[0]
        
        
    def available_bikes(self, number, time):
        '''
        Parameter(s): ID of station, logged time (strings).
        Returns: Available bikes based on station ID and logged time specified. 
        '''
        # Retrieves available bikes based on the number of the station and the time(epoch time)[2]. 
        query = self.conn.execute('SELECT available_bikes FROM dynamic WHERE number = :number AND logged = :time ', {'number':number, 'time':time})
        for row in query:
            return row[0]
        
    def status (self, number, time):
        '''
        Parameter(s): ID of station, logged time (strings).
        Returns: Status based on station ID and logged time specified. 
        '''
        # Retrieves status of station based on the number of the station and the time(epoch time)[2].
        query = self.conn.execute('SELECT status FROM dynamic WHERE number = :number AND logged = :time ', {'number':number, 'time':time})
        for row in query:
            return row[0]
            
    def num_bike_stands(self, number, time):
        '''
        Parameter(s): ID of station, logged time (strings).
        Returns: Number of bikes stands based on station ID and logged time specified
        (number of bike stands may change if more are added/ some are out of order etc.). 
        '''
        # Retrieves the number of bike stands at station based on the number of the station and the time(epoch time)[2].
        query = self.conn.execute('SELECT bike_stands FROM dynamic WHERE number = :number AND logged = :time ', {'number':number, 'time':time})
        for row in query:
            return row[0]
            
    def latest_time_logged(self, number):
        '''
        Parameter(s): ID of station (string).
        Returns: Latest time that data on bikes was logged based on station ID. 
        '''
        # Retrieves the latest time that data on the station was logged based on the number of the station[2].
        query = self.conn.execute('SELECT logged FROM dynamic WHERE number = :number', {'number':number})    
        times = []
        for row in query:
            times.append(row[0])
        last_time = int(times[-1])
        #https://docs.python.org/2/library/time.html
        # Converting epoch time into readable time [3]. 
        last_update = time.ctime(last_time)
        return last_update
            
    def num_bike_stations(self):
        '''
        Returns: Number of bike stations. 
        '''
        # Retrieves the number of bikes stations[2][4].
        query = self.conn.execute('SELECT COUNT(DISTINCT number) FROM dynamic')
        for row in query:
            return row[0]
            
    def take_credit(self, number):
        '''
        Parameter(s): ID of station (string).
        Returns: True if station takes credit card, or false if it does not. 
        '''
        # Returns true if station takes credit cards.[2]
        query = self.conn.execute('SELECT banking FROM static WHERE number = :number', {'number':number})
        for row in query:
            if row[0] == 'False':
                return False
            else:
                return True

    def get_historical_info_by_id(self, id):
        '''
        Parameter(s): ID of station (id or list).
        Returns: an array of dictionaries containing occupancy data, day, hour and minute
        '''
        # the keys to fetch
        keys = ["number", "bike_stands", "available_bike_stands", "available_bikes", "day", "hour", "minute"]

        query = self.QueryBuilder().select(keys, "dynamic").where([
            ["number", "=", id]
        ]).getQuery()

        c = self.conn.cursor()

        c.execute(query["sql"], query["values"])
        items = c.fetchall()

        # labels each result
        grouped_items = [self.label_results(keys, item) for item in items]

        return grouped_items


    def get_historical_info_by_id_and_day(self, id, day):
        '''
        Parameter(s): ID of station (id or list).
        Returns: an array of dictionaries containing occupancy data, day, hour and minute
        '''
        # the keys to fetch
        keys = ["number", "bike_stands", "available_bike_stands", "available_bikes", "day", "hour", "minute"]

        query = self.QueryBuilder().select(keys, "dynamic").where([
            ["number", "=", id], ["day", "=", day]
        ]).getQuery()

        c = self.conn.cursor()

        c.execute(query["sql"], query["values"])
        items = c.fetchall()

        # labels each result
        grouped_items = [self.label_results(keys, item) for item in items]

        return grouped_items
            
    
    def __ct__(self, log_time):
        return datetime.datetime.fromtimestamp(int(log_time)).strftime('%Y-%m-%d %H:%M:%S')
        # http://stackoverflow.com/questions/3682748/converting-unix-timestamp-string-to-readable-date-in-python
 
    def convert_time(self):
        c = self.conn.cursor()
        c.execute("SELECT logged FROM dynamic")
        result = c.fetchall()
        times = []
        for i in range(len(result)):
            times.append(self.__ct__(result[i][0]))
        return times

    def get_day_and_time(self, timestamp):
        m_date = datetime.datetime.fromtimestamp(timestamp)
        # this will get the week day from the date object
        # note these are integer indexes. Monday is 0, Tues is 1, Wed 2 etc
        day = m_date.weekday()

        hour = m_date.hour
        minute = m_date.minute
        # normalisation code if needed. I checked. Doesn't seem to be a problem
        # if 0 <= m_date.minute < 10:
        #     # its around the hour (00) mark
        #     minute = 0
        # elif 15 <= m_date.minute < 25:
        #     minute = 15
        # elif 30 <= m_date.minute < 40:
        #     minute = 30
        # else:
        #     minute = 45

        return (day, hour, minute)

    def num_unique_days(self):
        c = self.conn.cursor()
        query = c.execute("SELECT distinct day FROM dynamic")
        items = c.fetchall()
        return items


    def add_time_to_db(self):
        c = self.conn.cursor()
        # this isn't necessary once the database is updated
        # c.execute("ALTER TABLE dynamic ADD COLUMN 'date_time' 'String' ")
        #
        # @Luke the problem is somewhere here. times should be a list of string containing dtea/time
        # the list comprehension wraps every string in a tuple to allow the sqlite function to work
        # not getting any errors, just running infinitely for me.
        # also once you run this once, you'll get an error about the column date_time already existing (see above as to why this was happening)

        # this query will fetch unique rows. No station of a certain number will be logged at the same time as other stations of the same number
        query = c.execute("SELECT logged, number FROM dynamic")
        items = c.fetchall()
        #print(items)
        for item in items:
            info = self.get_day_and_time(item[0])

            # print((info[0], info[1], info[2], item[1], item[0]))
            # print(info)
            # print(item)
            # self.conn.execute("UPDATE dynamic SET day = " + str(info[0]) + ", hour = " + str(info[1]) + ", minute = " + str(info[2]) + "WHERE")
            query = "UPDATE dynamic SET day = " + str(info[0]) + \
            ", hour = " + str(info[1]) + \
            ", minute = " + str(info[2]) + \
            " WHERE number = " + str(item[1]) + \
            " AND logged = " + str(item[0])
            #print(query)

            self.conn.execute(query)
            self.conn.commit()

    def get_valid_real_time_count(self):
        c = self.conn.cursor()
        current_time = time.time()
        query = self.QueryBuilder().count(["number"], "real_time").where(
            [["updated", ">", current_time - 60]]).getQuery()
        print(query)
        count = c.execute(query["sql"], query["values"]).fetchall()[0][0]
        return count

    def insert_new_real_time_values(self, data, update = False):
        '''
        Parameter(s): a list of python dictionaries to add to the database
        Returns: Nothing. Updates values in the table
        '''
        db = dbQueries("bikes.db")
        c = self.conn.cursor()
        for d in data:
            new_data = {
                "number": d["number"],
                "available_bikes" : d["available_bikes"],
                "available_bike_stands" : d["available_bike_stands"],
                "bike_stands" : d["bike_stands"],
                "status": d["status"],
                "updated": int(time.time())
            }
            # check if the data exists
            if (not self.exists(d["number"], "real_time")) or update:
                # insert the data
                print("fetching new data")
                query = db.QueryBuilder().insert([key for key in new_data], [[new_data[key] for key in new_data]], "real_time").getQuery()
                c.execute(query["sql"], query["values"])
                self.conn.commit()

            else:
                query = db.QueryBuilder().update([key for key in new_data], [new_data[key] for key in new_data], "real_time").where(
                    [["number", "=", d["number"]]]
                ).getQuery()
                c.execute(query["sql"], query["values"])
                self.conn.commit()



    def get_real_time(self, number = None):
        # check if data is valid
        c = self.conn.cursor()
        label_keys = ["number", "name", "available_bike_stands", "bike_stands", "available_bikes", "status"]
        keys = ["real_time.number", "name", "available_bike_stands", "real_time.bike_stands", "available_bikes", "status"]
        if number is None:
            # get all
            query = self.QueryBuilder().select(keys, "real_time")\
                .join("static", "real_time.number", "static.number").getQuery()
        else:
            # get that station
            query = self.QueryBuilder().select(keys, "real_time")\
                .join("static", "real_time.number", "static.number")\
                .where([["real_time.number", "=", number]]).getQuery()

        print(query)
        results = c.execute(query["sql"], query["values"]).fetchall()
        print(results)
        grouped_items = [self.label_results(label_keys, item) for item in results]

        return grouped_items

    def close_connection(self):
        '''
        Parameter(s): None
        Returns: None. Closes the database connection for thread safe usage
        '''
        self.conn.close()
        
if(__name__ == "__main__"):
    db = dbQueries("../bikes.db")
    print(db.latest_time_logged(10))
    print(db.num_unique_days())
    print(db.get_historical_info_by_id(12))
    print(db.QueryBuilder().update(["number", "name"], ["10", "bob"], "mTable").where(
        [["name", "=", "bob"]]
    ).getQuery())
    # db.add_time_to_db()

