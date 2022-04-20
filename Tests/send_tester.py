import socket
import json
from time import sleep

port = 12345


# Send data to server
def send_sensors():
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect(("192.168.0.193", port))
    data = {

    }

    json_data = json.dumps(data)
    clientSocket.sendall(json_data.encode('utf-8'))
    clientSocket.close()

def send_request():
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect(("192.168.0.193", port))
    jdata = json.dumps({"type": 1}) 
    clientSocket.sendall(jdata.encode('utf-8'))
    # response = clientSocket.recv(1024).decode('utf-8')
    # print(response)
    clientSocket.close()


while True:
    send_sensors()
    sleep(3)

