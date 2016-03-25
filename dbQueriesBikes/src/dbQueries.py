# References:
#[1] "11.13. Sqlite3 — DB-API 2.0 Interface For Sqlite Databases — Python 2.7.11 Documentation". 
#     Docs.python.org, available: https://docs.python.org/2/library/sqlite3.html [Accessed: 25/03/16]

#[2] "Sqlite3 – Embedded Relational Database - Python Module Of The Week". Pymotw.com,
#     available: https://pymotw.com/2/sqlite3/ [Accessed: 25/03/16]

#[3] "15.3. Time — Time Access And Conversions — Python 2.7.11 Documentation". Docs.python.org, 
#     available: https://docs.python.org/2/library/time.html [Accessed: 25/03/16]
   
#[4] "SQL COUNT() Function". W3schools.com, 
#     available: http://www.w3schools.com/sql/sql_func_count.asp [Accessed: 25/03/16]

__author__ = "Ellen Rushe"

import sqlite3
import time

class dbQueries:
    
    def __init__(self, database_name):
        '''Connect to database[1]'''
        self.conn = sqlite3.connect(database_name)
        
    def station_to_ID(self, name):
        '''
        Parameter(s): Name of station (string).
        Returns: Number of station based on the name of the station.
        '''
        # If name is entered in lowercase or otherwise it will be converted to uppercase. 
        name.upper
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

