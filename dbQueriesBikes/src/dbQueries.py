import sqlite3
import time

class dbQueries:
    
    def __init__(self, database_name):
        # https://docs.python.org/2/library/sqlite3.html
        self.conn = sqlite3.connect(database_name)
        
    def station_to_ID(self, name):
        name.upper
        query = self.conn.execute('SELECT number FROM static WHERE name = :name', {'name':name})
        for row in query:
            return row[0]
        
    def station_address_by_name(self, name):  
        query = self.conn.execute('SELECT address FROM static WHERE name = :name', {'name':name})
        for row in query:
            return row[0]
        
    def station_address_by_ID(self, number):
        query = self.conn.execute('SELECT address FROM static WHERE number = :number', {'number':number})
        for row in query:
            return row[0]
        
    def station_coordinates_by_name(self, name):
        query = self.conn.execute('SELECT position_long, position_lat FROM static WHERE name = :name', {'name':name})
        for row in query:
            return row
        
    def station_coordinates_by_ID (self, number):
        query = self.conn.execute('SELECT position_long, position_lat FROM static WHERE number = :number', {'number':number})
        for row in query:
            return row  

    def available_bike_stands(self, number, time):
        # https://pymotw.com/2/sqlite3/
        query = self.conn.execute('SELECT available_bike_stands FROM dynamic WHERE number = :number AND logged = :time ', {'number':number, 'time':time})
        for row in query:
            return row[0]
        
        
    def available_bikes(self, number, time):
        # https://pymotw.com/2/sqlite3/
        query = self.conn.execute('SELECT available_bikes FROM dynamic WHERE number = :number AND logged = :time ', {'number':number, 'time':time})
        for row in query:
            return row[0]
        
    def status (self, number, time):
        # https://pymotw.com/2/sqlite3/
        query = self.conn.execute('SELECT status FROM dynamic WHERE number = :number AND logged = :time ', {'number':number, 'time':time})
        for row in query:
            return row[0]
            
    def num_bike_stands(self, number, time):
        # https://pymotw.com/2/sqlite3/
        query = self.conn.execute('SELECT bike_stands FROM dynamic WHERE number = :number AND logged = :time ', {'number':number, 'time':time})
        for row in query:
            return row[0]
            
    def latest_time_logged(self, number):
        # https://pymotw.com/2/sqlite3/
        query = self.conn.execute('SELECT logged FROM dynamic WHERE number = :number', {'number':number})    
        times = []
        for row in query:
            times.append(row[0])
        last_time = int(times[-1])
        #https://docs.python.org/2/library/time.html
        last_update = time.ctime(last_time)
        return last_update
            
    def num_bike_stations(self):
        # https://pymotw.com/2/sqlite3/
        # http://www.w3schools.com/sql/sql_func_count.asp
        query = self.conn.execute('SELECT COUNT(DISTINCT number) FROM dynamic')
        for row in query:
            return row[0]
            
    def take_credit(self, number):
        # https://pymotw.com/2/sqlite3/
        query = self.conn.execute('SELECT banking FROM static WHERE number = :number', {'number':number})
        for row in query:
            if row[0] == 'False':
                return False
            else:
                return True

