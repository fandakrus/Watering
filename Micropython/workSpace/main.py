import network
from time import sleep
from machine import Pin
try:
  import usocket as socket 
except:
  import socket
import json
  

def do_connect():
    # connect to speciefied wifi
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('ssis', 'passwd')
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())
    
def send(data, require_response=False):
    # send data to required server
    try:
      server = socket.socket()
      server.connect(('192.168.0.193', 12345))
      # start socket object and connect to server
      server.sendall(data.encode('utf-8'))
      # if reqular request is sended respons is waited for
      if require_response:
          data = server.recv(1024)
          server.close()
          return data
      server.close()
      
    except OSError as e:
        print(e)
    
    
def main():
   do_connect()
   counter = 0
   while True:
      if counter == 360:
        data = json.dumps(measure())
        send(data)
      else:
        response = send(json.dumps({"type": 1}), require_response=True)
        print(response)
      sleep(5)
        
   
   
main()

