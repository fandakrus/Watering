import socket

port = 12345

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

clientSocket.connect(("127.0.0.1",port))

 

# Send data to server

data = "Hello Server!"

clientSocket.send(data.encode('utf-8'))