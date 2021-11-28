import socket
import json
from datetime import datetime
from time import sleep

def write_to_database(data):
    pass

def is_valid(data):
    # confirm if data are ok recieved 
    pass


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
                    c.send('200')
                else:
                    c.send('500')
                self.rcvData = None
                self.results = None
                c.close()



    def pawel(self):
        print('pawel')
        sleep(4)

        
def main():
    # creates new measurement unit
    meas = Meassurement()
    # let socket listen while other things happen
    meas.listen()


if __name__ == "__main__":
    main()