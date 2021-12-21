import network
from time import sleep
from machine import Pin
try:
  import usocket as socket 
except:
  import socket
import json


def check_pin(pin, value):
  if pin.value() != value:
   # print(value)
   pin.value(value) 


class Watering:
  def __init__(self):
    self.main_valve_pin = Pin(32, Pin.OUT)
    self.circle1_pin = Pin(33, Pin.OUT)
    self.circle2_pin = Pin(25, Pin.OUT)
    self.circle3_pin = Pin(26, Pin.OUT)
    self.circle4_pin = Pin(27, Pin.OUT)
    
  def set_pins(self, data):
    try:
      check_pin(self.main_valve_pin, data["main_valve"])
      check_pin(self.circle1_pin, data["circle1"])
      check_pin(self.circle2_pin, data["circle2"])
      check_pin(self.circle3_pin, data["circle3"])
      check_pin(self.circle4_pin, data["circle4"])
    except TypeError:
      print("Hagabuga ind")
    

def do_connect():
    # connect to speciefied wifi
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('ssid', 'passwd')
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
          data = server.recv(1024).decode('utf-8')
          server.close()
          return data
      server.close()
      
    except OSError as e:
        print(e)
    
    
def main():
   watering = Watering()
   do_connect()
   counter = 0
   while True:
      if counter == 360:
        data = json.dumps(measure())
        send(data)
      else:
        response = send(json.dumps({"type": 1}), require_response=True)
        unjsoned_resp = json.loads(response)
        print("circle ")
        print(unjsoned_resp)
        watering.set_pins(unjsoned_resp)
      sleep(5)
        
   
   
main()


