# creates a database to hold the information of the users and the plants
import mysql.connector
from mysql.connector import errorcode
from datetime import date, datetime, timedelta


#connecting with the Server
try:
  cnx = mysql.connector.connect(user='user',
                                password='password',
                                database='WateringSystem',
                                host='127.0.0.1')
###################### IMPORTANT ######################
# CHANGE THE USERNAME AND PASSWORD INTO VALID ONES
# FOR THE PROGRAM TO WORK CORRECTLY
 
  cursor = cnx.cursor()
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)


#declaring the database name    
DB_NAME = 'WateringSystem'


#the tables that are going to be used in the database
TABLES = {}

TABLES['gardeners'] = (
    "CREATE TABLE `gardeners` ("
    "  `gardener_no` int(11) NOT NULL AUTO_INCREMENT,"
    "  `username` varchar(14) NOT NULL,"
    "  `password` varchar(20) NOT NULL,"
    "  `first_name` varchar(14) NOT NULL,"
    "  `last_name` varchar(16) NOT NULL,"
    "  PRIMARY KEY (`gardener_no`)"
    ") ENGINE=InnoDB")

TABLES['plants'] = (
    "CREATE TABLE `plants` ("
    "  `plant_no` int(11) NOT NULL AUTO_INCREMENT,"
    "  `gardener_no` int(11) NOT NULL,"
    "  `plant_cname` varchar(20) NOT NULL,"
    #"  `plant_sname` varchar(50) NOT NULL,"
    "  PRIMARY KEY (`plant_no`), "
    "  CONSTRAINT `plants_ibfk_1` FOREIGN KEY (`gardener_no`)"
    "     REFERENCES `gardeners` (`gardener_no`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")

TABLES['soil_humidity'] = (
    "CREATE TABLE `soil_humidity` ("
    "  `humidity_no` int(20) NOT NULL AUTO_INCREMENT,"
    "  `plant_no` int(11) NOT NULL,"
    "  `measurement_date` datetime NOT NULL,"
    "  `humidity_value` int(4) NOT NULL,"
    #"  PRIMARY KEY (`plant_no`), "
    "  PRIMARY KEY (`humidity_no`), "
    "  CONSTRAINT `humidity_ibfk_1` FOREIGN KEY (`plant_no`)"
    "     REFERENCES `plants` (`plant_no`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")

TABLES['water_consumption'] = (
    "CREATE TABLE `water_consumption` ("
    "  `plant_no` int(11) NOT NULL,"
    "  `measurement_date` datetime NOT NULL,"
    "  `consumption_value` int(11) NOT NULL,"
    "  PRIMARY KEY (`plant_no`), "
    "  CONSTRAINT `consumption_ibfk_1` FOREIGN KEY (`plant_no`)"
    "     REFERENCES `plants` (`plant_no`) ON DELETE CASCADE"
    ") ENGINE=InnoDB")


#creating the database if it does not exist
def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

try:
    cnx.database = DB_NAME  
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        cnx.database = DB_NAME
    else:
        print(err)
        exit(1)


#creating the tables if they do not exist
for name, ddl in TABLES.items():
    try:
        print("Creating table {}: ".format(name), end='')
        cursor.execute(ddl)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")


#creating variables used for inserting the data into the database
add_gardener = ("INSERT INTO gardeners "
                "(username, password, first_name, last_name)"
                "VALUES (%s, %s, %s, %s)")

add_plant = ("INSERT INTO plants "
             "(gardener_no, plant_cname)"
             "VALUES (%s, %s)")

add_humidity = ("INSERT INTO soil_humidity "
                "(plant_no, measurement_date, humidity_value)"
                " VALUES (%s, %s, %s)")

#use the functions as below

data_gardener1 = ('groot', '123456','SPECX', 'Team')

#inserting the gardeners data into the database
cursor.execute(add_gardener, data_gardener1)
#print(getLastID('gardeners', 'gardener_no'))


# used for adding plants to the database
'''
#getting the id of the last row which is also the garderner's id
gardener_no = cursor.lastrowid

data_plant1 = (gardener_no, "Daisy")
data_plant2 = (gardener_no, "Strawberry")

cursor.execute(add_plant, data_plant1)
plant_no = cursor.lastrowid
measurement_date = datetime.now()
data_humidity1 = (plant_no, measurement_date, '89')
cursor.execute(add_humidity, data_humidity1)

cursor.execute(add_plant, data_plant2)
plant_no = cursor.lastrowid
measurement_date = datetime.now()
data_humidity2 = (plant_no, measurement_date, '70')
cursor.execute(add_humidity, data_humidity2)

'''



#commiting the data 
cnx.commit()


#cursor.close()
#cnx.close()
