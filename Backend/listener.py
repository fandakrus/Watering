import socket
import json
import mariadb

def write_to_database(data):
    # takes given data and write it to database on rpi
    try:                         #connect to database -  password needs to be inserted
        conn = mariadb.connect(
            user="root",
            password="Thigelis2",
            host="localhost",
            port=3306,
            database="watering"
    )
        print("Connected to database")
    # if connection fails
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
    # create cursor object on given connection
    curr = conn.cursor()
    # insert values to database
    try:
        curr.execute("INSERT INTO sensors(soil_humidity, water_height) VALUES (?, ?)", (data["soil_humidity"], data["water_height"]))
    except mariadb.Error as e:
        print(f"Could not write in data because of error: {e}")
    # makes the changes in given database
    conn.commit()
    # end the connection to database
    conn.close()
    

def is_valid(data):
    return True



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