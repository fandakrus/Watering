import mariadb
from config import conn, logging


def write_to_database(data):
    curr = conn.cursor()
    # insert values to database
    try:
        curr.execute("INSERT INTO sensors(soil_humidity, water_height, float_sensor) VALUES (?, ?, ?)",
                     (data["soil_humidity"], data["water_height"], data["float_sensor"]))
        logging.info("Sensor data succesfully written in db")
    except mariadb.Error as e:
        logging.error(f"Could not write into sensors database because of error: {e}")
    # makes the changes in given database
    conn.commit()


def value_check(value):
    # check if value is in some reasonable interval
    bottom_border = 0
    upper_border = 10000
    if value > bottom_border and value < upper_border:
        return True
    else:
        logging.error("Values out of range")
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
