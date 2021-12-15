import mariadb
import logging
from sensors import database_connect
import datetime
import json


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
        logging.error(f"Could not get data from database: {e}")
    # parse values to lists by type to be returned
    for (id, soil_humidity, water_height) in curr:
        soil_list.append(soil_humidity)
        water_list.append(water_height)
    # cleare the cursor object to select new data
    useless_data = curr.fatchall()
    try:
        curr.execute("SELECT id, float_sensor FROM sensors ORDER BY id DESC LIMIT 1")
    except mariadb.Error as e:
        logging.error(f"Could not get data from database: {e}")
    id, float_sensor = curr.fatchone()
    conn.close()
    return(soil_list, water_list, float_sensor)


def read_controls_database():
    # return last line from db with conrols records
    conn = database_connect("watering", 50)
    curr = conn.cursor()
    try:
        curr.execute(f"SELECT id, main_control, circle1, circle2, circle3, circle4 FROM controls ORDER BY id DESC LIMIT 1")
    except mariadb.Error as e:
        print(f"Could not get data from database: {e}")
    data = curr.fetchone()
    conn.close()
    return data

def process_cycles(cur_cycle):
    cycle_list = [0] * 4
    if cur_cycle is not None:
        cycle_list[cur_cycle] = 1
    return_data = {
                "circle1": cycle_list[0],
                "circle2": cycle_list[1],
                "circle3": cycle_list[2],
                "circle4": cycle_list[3],
            }
    return return_data

def check_main_valve(data):
    values = list(data.values())
    if any(values):
        data["main_valve"] = True
    else:
        data["main_valve"] = False
    return json.dumps(data)


class Watering():
    """
    Class handles is called on reqular requst and returns back value what should be watered
    """
    def __init__(self) -> None:
        # if the module is auto watering variables are used to control the run
        self.is_watering_automaticaly = False
        self.current_circle = None
        self.current_circle_starting_time = None
        # variable used to decide if it is first request after 2:00 AM
        self.watered_auto_today = False
        # how long one circle should be watered in seconds
        self.circle_duration = 600


    def check_controls(self):
        # takes data from db with records from web ui and return it if something is set to be watered
        id, main_control, circle1, circle2, circle3, circle4 = read_controls_database()
        if (main_control):
            return_data = {
                "circle1": int(circle1),
                "circle2": int(circle2),
                "circle3": int(circle3),
                "circle4": int(circle4),
            }
            return return_data
        return False

    def start_water(self):
        """
        In the right time finds out if it should start waterin by given conditions
        """
        # reads last 20 values measured by sensors
        soil_list, water_list, float_sensor = read_sensor_database(20)
        if True:
            return self.water_run()
        else:
            return False


    def water_run(self):
        """
        Maneges the run of watering - if it should start begins and then check the duration for each valve 
         - returns same dict as controls check
        """
        if self.current_circle is None:
            self.current_circle = 1
            self.current_circle_starting_time = datetime.datetime.now()
        elif (datetime.datetime.now() - self.current_circle_starting_time).total_seconds() >= self.circle_duration:
            if self.current_circle == 4:
                # ends the watering cycle
                self.current_circle = None
                self.current_circle_starting_time = None
                self.is_watering_automaticaly = False
            else:
                self.current_circle += 1
                self.current_circle_starting_time = datetime.datetime.now()
        return process_cycles(self.current_circle)

    def check_auto(self):
        if self.is_watering_automaticaly:
            return self.water_run()
        now = datetime.datetime.now()
        if now.hour == 2 and not self.watered_auto_today:
            logging.info("Automatic watering was triggered")
            self.watered_auto_today = True
            return self.start_water()
        elif now.hour == 0 and self.watered_auto_today:
            self.watered_auto_today = False

    def handle_reqular_request(self, data):
        # main funcion imported to script
        controls_value = self.check_controls()
        if(controls_value):
            return check_main_valve(controls_value)
        auto_value = self.check_auto()
        if(auto_value):
            return check_main_valve(auto_value)
        

if __name__ == '__main__':
    watering = Watering()
    print(watering.handle_reqular_request("plesk"))
    

