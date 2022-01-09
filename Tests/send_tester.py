import socket
import json

port = 12345

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

clientSocket.connect(("192.168.0.193", port))

 

# Send data to server

data = {
    "type": "0",
    "soil_humidity": 10,
    "water_height": 58.4,
    "float_sensor": True
}

json_data = json.dumps(data)

clientSocket.sendall(json_data.encode('utf-8'))