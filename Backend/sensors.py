import logging
import mariadb
from time import sleep
import sys


# configure logging to given file for better bug finding
logging.basicConfig(filename="/var/log/python-log/error-log", filemode="w", level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

def database_connect(name, count):
    # connects to db and return given connection object
    try:
        conn = mariadb.connect(
            user="root",
            password="",
            host="localhost",
            port=3306,
            database=name
        )
        logging.info(f"Successfully connected to database {name}")
    # if connection fails
    except mariadb.Error as e:
        if count <= 100:
            logging.critical("Could not connect to DB")
            sys.exit(1)
        logging.error(f"Error connecting to MariaDB Platform: {e}")
        count += 1
        sleep(5)
        # dangerous!! can cycle forever if connection is not made exit program
        return database_connect(name, count)
    # return connection to given database
    return conn


def write_to_database(data):
    # write data from sensors to database
    conn = database_connect("watering", 0)
    curr = conn.cursor()
    # insert values to database
    try:
        curr.execute("INSERT INTO sensors(soil_humidity, water_height, float_sensor) VALUES (?, ?, ?)",
                     (data["soil_humidity"], data["water_height"], data["float_sensor"]))
        logging.info("Sensor data succesfully written in db")
    except mariadb.Error as e:
        logging.error(f"Could not write in data because of error: {e}")
    # makes the changes in given database
    conn.commit()
    # end the connection to database
    conn.close()


def value_check(value):
    # check if value is in some reasonable interval
    bottom_border = 0
    upper_border = 10000
    if value > bottom_border and value < upper_border:
        return True
    else:
        return False


def is_valid(data):
    # check validity of data and return it to request data again or not
    try:
        if value_check(data["water_height"]) and value_check(data["soil_humidity"]):
            if data["float_sensor"] == True or data["float_sensor"] == False:
                return True
    except KeyError:
        logging.error("Invalid params received")
        return False

# most import func here control the others
def handle_sensors(data):
    # there is tested if data are correct and then are writen to the database
        if is_valid(data):
            data["soil_humidity"] = float(data["soil_humidity"])
            data["water_height"] = float(data["water_height"])
            write_to_database(data)
            return True
        else:
            return False
            