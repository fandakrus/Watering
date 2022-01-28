import socket
import json
from config import logging
from sensors import handle_sensors
from watering import Watering


class Listening():

    def __init__(self) -> None:
        #watering class used to handle data
        self.watering = Watering()
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
                print(f"Connetion recived from {addr} and data is {self.rcvData}")
                logging.info(f"Connetion recived from {addr} and data is {self.rcvData}")
                # if esp is expecting response send it
                response = self.handle_data()
                if response is not None:
                    c.sendall(response.encode('utf-8'))
                self.rcvData = None
                self.results = None
                c.close()

    def handle_data(self):
        # makes from recived json file data to further use
        self.results = json.loads(self.rcvData.decode('utf-8'))
        # find what kind of data were ricieved
        try:
            type = int(self.results["type"])
        except KeyError:
            return None
        # decide what script should run with given data  
        # recives 0 for sensors data 
        # and 1 for regular request   
        if type == 0:
            handle_sensors(self.results)
            return None
        elif type == 1:
            return self.watering.handle_reqular_request(self.results)
        else:
            return None
    


    

def main():
    # creates new listening unit
    listening = Listening()
    # let socket listen while other things happen
    listening.listen()


if __name__ == "__main__":
    main()
