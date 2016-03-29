# Reference:
# Nose.readthedocs.org. 'Writing Tests - Nose 1.3.7 Documentation', available: 
# https://nose.readthedocs.org/en/latest/writing_tests.html [Accessed: 25/03/16]

__author__ = "Ellen Rushe"

from src.dbQueries import dbQueries

# Test using 'bikes' database.
dbq = dbQueries('test_db_bikes.db')

def test_station_to_ID():
    assert dbq.station_to_ID('BLACKHALL PLACE')==88
    
def test_station_address_by_name():
    assert dbq.station_address_by_name('BLACKHALL PLACE')== 'Blackhall Place'

def test_station_address_by_ID():
    assert dbq.station_address_by_ID('88')== 'Blackhall Place'

def test_station_coordinates_by_name():
    assert dbq.station_coordinates_by_name('BLACKHALL PLACE')== (-6.281637, 53.3488)
  
def test_station_coordinates_by_ID ():
    assert dbq.station_coordinates_by_ID('88')== (-6.281637, 53.3488)

def test_available_bike_stands():
    assert dbq.available_bike_stands('42', '1457367302')== 18
 
 
def test_available_bikes():
    assert dbq.available_bikes('42', '1457367302')== 12
 
def test_status ():
    dbq.status('42', '1457367302')=='OPEN'
     
def test_num_bike_stands():
    assert dbq.num_bike_stands('42', '1457367302')==30
     
def test_latest_time_logged():
    dbq.latest_time_logged('88')=='Fri Mar 11 19:15:01 2016'
     
def test_num_bike_stations():
    assert dbq.num_bike_stations()==101

def test_take_credit():
    assert dbq.take_credit('88')==False and dbq.take_credit('33')==True
    

