import sys
import mariadb
import logging
from sensors import database_connect

is_watering_manualy = False
is_watering_automaticaly = False
watered_auto_today = False

#configure logging
logging.basicConfig(filename="/var/log/python-log/error-log", filemode="w", level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


def read_sensor_database(limit):
    # get limit rows from database with sensor data 
    soil_list = []
    water_list = []
    # makes connection to database with given method
    conn = database_connect("watering", 50)
    
    curr = conn.cursor()
    try:
        curr.execute(f"SELECT id, soil_humidity, water_height FROM sensors ORDER BY id DESC LIMIT {limit}")
    except mariadb.Error as e:
        print(f"Could not get data from database: {e}")
    # parse values to lists by type to be returned
    for (soil_humidity, water_height) in curr:
        soil_list.append(soil_humidity)
        water_list.append(water_height)
    conn.close()
    return(soil_list, water_list)


def read_controls_database():
    # return last line from db with conrols records
    conn = database_connect("watering", 50)
    curr = conn.cursor()
    try:
        curr.execute(f"SELECT id, main_control, circle1, circle2, circle3, circle4 FROM controls ORDER BY id DESC LIMIT 1")
    except mariadb.Error as e:
        print(f"Could not get data from database: {e}")
    return curr.fetchone()


def check_controls():
    # takes data from db with records from web ui and return it if something is set to be watered
    data = read_controls_database()
    if data["main_control"]:
        return_data = {
            "circle1": int(data["circle1"]),
            "circle2": int(data["circle2"]),
            "circle3": int(data["circle3"]),
            "circle4": int(data["circle4"]),
        }
        return return_data
    return False


def water():
    pass

def handle_reqular_request(data):
    # main funcion imported to script
    controls_value = check_controls()
    if(controls_value):
        return controls_value
    


