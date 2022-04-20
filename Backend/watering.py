import mariadb
import logging
import datetime
import json

from config import conn, logging
from history import CiclesHistory
from water_fall import WaterFallData

def ping_db(conn):
    try:
        conn.ping()
    except mariadb.DatabaseError as e:
        logging.error(f"Database connetion error occured: {e}, trying to reconenct ...")
        conn.reconnect()


def process_rain_fall():
    rain_class = WaterFallData()
    rain_class.get_html()
    rain_class.get_record()
    return rain_class.get_rain_value()


def read_sensor_database(limit):
    # get limit rows from database with sensor data 
    # function returns limit of values for soil_hum and water_height from db and one value for last float_sensor
    water_list = []
    ping_db(conn)
    # creates new cursor object to interact with db
    curr = conn.cursor()
    try:
        curr.execute(f"SELECT id, water_height FROM sensors ORDER BY id DESC LIMIT {limit}")
    except mariadb.Error as e:
        logging.error(f"Could not get data from database: {e}")
    # parse values to lists by type to be returned
    for (id, water_height) in curr:
        water_list.append(water_height)
    # cleare the cursor object to select new data
    curr.fetchall()
    conn.commit()
    try:
        curr.execute("SELECT id, float_sensor FROM sensors ORDER BY id DESC LIMIT 1")
    except mariadb.Error as e:
        logging.error(f"Could not get data from database: {e}")
    id, float_sensor = curr.fetchone()
    curr.fetchall()
    conn.commit()
    return(water_list, float_sensor)


def read_controls_database():
    # return last line from db with conrols records
    ping_db(conn)
    curr = conn.cursor()
    try:
        curr.execute(f"SELECT id, main_control, water_source, circle1, circle2, circle3, circle4 FROM controls ORDER BY id DESC LIMIT 1")
    except mariadb.Error as e:
        logging.error(f"Could not get data from database: {e}")
    # gets tuple of given variables to data
    data = curr.fetchone()
    # cleares connetion for new query
    curr.fetchall()
    conn.commit()
    return data


def process_cycles(cur_cycle):
    # get number of current cycle to return dict with desired format
    cycle_list = [0] * 4
    if cur_cycle is not None:
        cycle_list[cur_cycle - 1] = 1
    return_data = {
                "circle1": cycle_list[0],
                "circle2": cycle_list[1],
                "circle3": cycle_list[2],
                "circle4": cycle_list[3],
            }
    return return_data

def check_main_valve(data):
    # check if any value of circles is on to tell esp how to control the main valve -> json
    values = list(data.values())
    if any(values):
        data["main_valve"] = 1
    else:
        data["main_valve"] = 0
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
        # controls value used in rest of program
        self.main_control = False
        self.water_source = False
        self.empty_water_dict = {
            "circle1": 0,
            "circle2": 0,
            "circle3": 0,
            "circle4": 0,
        }
        # creates class to operete history db
        self.history = CiclesHistory()


    def check_controls(self):
        """
        With use of external function get all data from controls db 
        -> jsoned(Dict[main_valve<int>, ]
        """
        id, main_control, water_source, circle1, circle2, circle3, circle4 = read_controls_database()
        self.main_control = main_control
        self.water_source = water_source
        if any([circle1, circle2, circle3, circle4]):
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
        In the right time finds out if it should start watering by given conditions
        -> trigger watering function if wanted
        """
        # reads last 20 values measured by sensors
        water_list, float_sensor = read_sensor_database(20)
        try:
            rain_fall = process_rain_fall()
        except OSError as e:
            logging.error(f"Didn't get right rain_fall data from website selector and raise error: {e}")
            return False
        if True:
            self.is_watering_automaticaly = True
            return self.water_run()
        else:
            return False


    def water_run(self):
        """
        Maneges the run of watering - if it should start begins and then check the duration for each valve 
        -> Dict[main_valve<int>, circles<int>]
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
        """
        Decide when should the regular auto checked be performed (by time)
        -> triggers funcion to check values for auto water
        """
        if self.is_watering_automaticaly:
            return self.water_run()
        now = datetime.datetime.now()
        if now.hour == 0 and not self.watered_auto_today:
            logging.info("Automatic watering was triggered")
            self.watered_auto_today = True
            return self.start_water()
        # reset bool variable watered auto today so the automaitc watering is trigerred at night
        elif now.hour == 22 and self.watered_auto_today:
            self.watered_auto_today = False
        return None

    def handle_reqular_request(self, data):
        """
        Main funcion imported to script
        checks both auto and manual inputs
        -> jsoned(Dict[main_valve<int>, all controls<int>]) = procesed response to be sended 
        """
        controls_value = self.check_controls()
        # if the main switch is of don't water at all
        if not self.main_control:
            self.history.decide_history_database(self.empty_water_dict)
            return check_main_valve(self.empty_water_dict)
        # decides if water should be started based on manual controls
        if(controls_value):
            self.history.decide_history_database(controls_value)
            return check_main_valve(controls_value)
        auto_value = self.check_auto()
        if(auto_value):
            self.history.decide_history_database(auto_value)
            return check_main_valve(auto_value)
        self.history.decide_history_database(self.empty_water_dict)
        return check_main_valve(self.empty_water_dict)
        

if __name__ == '__main__':
    watering = Watering()
    print(watering.handle_reqular_request("plesk"))
    

