import mariadb
from config import connc, logging
from datetime import datetime


class CiclesHistory():
    """
    Class to control values of on each cirlce and takes action on changes and write important times to db
    """
    def __init__(self) -> None:
        # class holds list of values on cirlces
        self.circle_list = [False] * 4
        # if any cicles are watering starting time is stored here
        self.circle_time_list = [None] * 4

    def write_history_database(self, start_time, end_time, circle) -> None:
        # get record for the history db and insert it into db
        conn = connc.get_connecion()
        curr = conn.cursor()
        try:
            curr.execute("INSERT INTO watering_history(start_time, end_time, circle) VALUES (?, ?, ?)",
                        (start_time.strftime('%Y-%m-%d %H:%M:%S'), end_time.strftime('%Y-%m-%d %H:%M:%S'), circle))
            logging.info("Sensor data succesfully written in db")
        except mariadb.Error as e:
            logging.error(f"Could not write in data because of error: {e}")
        # makes the changes in given database
        conn.commit()            
    

    def decide_differance(self, db_value, act_value, index) -> bool:

        if db_value == bool(act_value):
            return False
        if db_value == False and bool(act_value) == True:
            # print("data changed value remebered")
            self.circle_time_list[index] = datetime.now()
            self.circle_list[index] = True
            return False
        return True


    def decide_history_database(self, data) -> None:
        """
        with use of decide_diff function prepare records to be inserted into history db based on values witch are returned prepared to send
        """
        data_list = [data["circle1"], data["circle2"], data["circle3"], data["circle4"]]
        # print(f"{data_list = }")
        # print(f"{self.circle_list = }")
        # print(f"{self.circle_time_list = }")
        for index, (db_value, act_value) in enumerate(zip(self.circle_list, data_list)):
            if self.decide_differance(db_value, act_value, index):
                # print("Writing")
                self.write_history_database(self.circle_time_list[index], datetime.now(), index + 1)
                self.circle_time_list[index] = None
                self.circle_list[index] = False
