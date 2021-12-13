import socket
import json
from time import sleep
import logging
from sensors import handle_sensors
from watering import Watering

# configure logging to given file for better bug finding
logging.basicConfig(filename="/var/log/python-log/error-log", filemode="w", level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


class Listening():

    def __init__(self) -> None:
        # port used for this communication is 12345
        self.port = 12345
        # make new socket used to listen to values from measurements
        self.m_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # this binds socket to given port
        self.m_socket.bind(('', self.port))
        # let socket listen and que up max 5 connections   
        self.m_socket.listen(5)
        #watering class used to handle data
        self.watering = Watering()

    def listen(self):
        # keep listening for the incoming traffic and handle the connections
        logging.info(f"Socket is listening on port {self.port}.")
        while True:
            c, addr = self.m_socket.accept()
            self.rcvData = c.recv(1024)
            # activate when message is received
            if self.rcvData is not None:
                # logging.info(f"Address {addr} connected.")
                if self.handle_data():
                    # c.send('200')
                    pass
                else:
                    # c.send('500')
                    pass
                self.rcvData = None
                self.results = None
                c.close()

    def handle_data(self):
        # makes from recived json file data to further use
        self.results = json.loads(self.rcvData.decode('utf-8'))
        # find what kind of data were ricieved
        try:
            self.type = self.results["type"]
        except KeyError:
            return False
        # decide what script should bye     
        if self.type == "sensors":
            return handle_sensors(self.results)
        elif self.type == "reqular-request":
            return self.watering.handle_reqular_request(self.results)
        else:
            return False
    


    

def main():
    # creates new listening unit
    listening = Listening()
    # let socket listen while other things happen
    listening.listen()


if __name__ == "__main__":
    main()
