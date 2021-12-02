import socket
import json
import mariadb
from time import sleep


def database_connect(name):
    # connects to db and return given connection object
    try:                         
        conn = mariadb.connect(
            user="root",
            password="",
            host="localhost",
            port=3306,
            database=name
    )
        print("Connected to database")
    # if connection fails
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sleep(5)
        # dangerous!! can cycle forever if connection is not made falls on recursion error
        return database_connect(name)
    # create cursor object on given connection
    return conn


def write_to_database(data):
    # write data from sensors to database
    conn = database_connect("watering")
    curr = conn.cursor()
    # insert values to database
    try:
        curr.execute("INSERT INTO sensors(soil_humidity, water_height) VALUES (?, ?)", (data["soil_humidity"]), data["water_height"])
    except mariadb.Error as e:
        print(f"Could not write in data because of error: {e}")
    # makes the changes in given database
    conn.commit()
    # end the connection to database
    conn.close()

"""
This function is probably useless

def percentige_check(key, value):
    number_list = []
    diff = 1000    # percentage that new value cant differ from the avrage
    conn = database_connect("watering")
    curr = conn.cursor()

    try:
        curr.execute(f"SELECT id, {key} FROM sensors ORDER BY id DESC LIMIT 20")
    except mariadb.Error as e:
        print(f"Could not get data from database: {e}")
    for number in curr:
        number_list.append(number)
"""


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
        if value_check(int(data["water_height"])) and value_check(int(data["soil_humidity"])):
            return True    
    except KeyError:
        return False    



class Meassurement():

    def __init__(self) -> None:
        # port used for this comunication is 12345
        self.port = 12345
        # make new socket used to listen to values from measurments
        self.m_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # this binds socket to given port
        self.m_socket.bind(('', self.port))
        # let socket listen and que up max 5 connections   
        self.m_socket.listen(5)        


    def listen(self):
        # keep listening for the incoming traffic and hendle the connections
        print(f"Socket is listening on port {self.port}.")
        while True:
            c, addr = self.m_socket.accept()
            self.rcvData = c.recv(1024)
            # activate when message is recieved
            if self.rcvData is not None:
                # makes from recived json file data to further use
                self.results = json.loads(self.rcvData.decode('utf-8'))
                print(self.results)
                # there is tested if data are corect and then are writen to the database
                if is_valid(self.results):
                    self.results["soil_humidity"] = int(self.results["soil_humidity"])
                    self.results["water_height"] = int(self.results["water_height"])
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