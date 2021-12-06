import socket
import json
import mariadb
from time import sleep
import logging
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
        # dangerous!! can cycle forever if connection is made exit program
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


class Meassurement():

    def __init__(self) -> None:
        # port used for this communication is 12345
        self.port = 12345
        # make new socket used to listen to values from measurements
        self.m_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # this binds socket to given port
        self.m_socket.bind(('', self.port))
        # let socket listen and que up max 5 connections   
        self.m_socket.listen(5)

    def listen(self):
        # keep listening for the incoming traffic and handle the connections
        logging.info(f"Socket is listening on port {self.port}.")
        while True:
            c, addr = self.m_socket.accept()
            self.rcvData = c.recv(1024)
            # activate when message is received
            if self.rcvData is not None:
                # makes from recived json file data to further use
                self.results = json.loads(self.rcvData.decode('utf-8'))
                # there is tested if data are correct and then are writen to the database
                if is_valid(self.results):
                    self.results["soil_humidity"] = float(self.results["soil_humidity"])
                    self.results["water_height"] = float(self.results["water_height"])
                    write_to_database(self.results)
                    # c.send('200')
                else:
                    pass
                    # c.send('500')
                self.rcvData = None
                self.results = None
                c.close()


def main():
    # creates new measurement unit
    meas = Meassurement()
    # let socket listen while other things happen
    meas.listen()


if __name__ == "__main__":
    main()
