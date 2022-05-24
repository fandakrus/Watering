import network
from time import sleep
from machine import Pin, ADC, WDT
try:
  import usocket as socket 
except:
  import socket
import json
# not defaul lib needs to be upload on ESP
from hcsr04_lib import HCSR04
import gc

well_hight = 150
# analog output from moisture sensor shut be connected to this pin
moisture_sensor_pin = ADC(Pin(34))   
moisture_sensor_pin.atten(ADC.ATTN_11DB)
# connects sensor with trig pin on GPI12 and echo pin on GPIO14
# timeout set to 20000 for longer distances measurement
hcsr04_sensor = HCSR04(trigger_pin=12, echo_pin=14, echo_timeout_us=50000)
float_sensor = Pin(35, Pin.IN, Pin.PULL_DOWN)
gc.enable()
wdt = WDT(timeout=50000)


def value_change(value):
    if value:
        return 0
    return 1

def check_pin(pin, value):
  if pin.value() == value:
   # print(value)
   pin.value(value_change(value))
   

def measure():
    humidity_values = [0] * 5
    # gets 5 values from moisture sensor
    for i in range(len(humidity_values)):
        humidity_values[i] = moisture_sensor_pin.read()
        sleep(0.5)
    # gets distance from water surface
    distance = hcsr04_sensor.distance_cm()
    data = {
        "type": 0,
        "soil_humidity": sum(humidity_values) / len(humidity_values),
        "float_sensor": float_sensor.value(),
        "water_height": well_hight - distance,
        }
    print(f"sending data {data}")
    return data


class Watering:
  def __init__(self):
    self.main_valve_pin = Pin(32, Pin.OUT, value=1)
    self.circle1_pin = Pin(33, Pin.OUT, value=1)
    self.circle2_pin = Pin(25, Pin.OUT, value=1)
    self.circle3_pin = Pin(26, Pin.OUT, value=1)
    self.circle4_pin = Pin(27, Pin.OUT, value=1)
    
  def set_pins(self, data):
      # for each pin used check its value and change it based on recieved data
    try:
      check_pin(self.main_valve_pin, data["main_valve"])
      check_pin(self.circle1_pin, data["circle1"])
      check_pin(self.circle2_pin, data["circle2"])
      check_pin(self.circle3_pin, data["circle3"])
      check_pin(self.circle4_pin, data["circle4"])
    except TypeError:
      print("Did not recieved required data from server")
    

def do_connect():
    # connect to speciefied wifi
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('SSID', 'passwd')
        while not sta_if.isconnected():
            pass
    wdt.feed()
    print('network config:', sta_if.ifconfig())
    
def send(data, require_response=False):
    # send data to required server`
    
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
   # connects to wifi on boot up
   do_connect()
   counter = 0
   while True:
      wdt.feed()
      if counter == 0:
        data = json.dumps(measure())
        send(data)
        sleep(2)
        wdt.feed()
      # get data for each cyrcle and decide wheter is sould changes values on pins
      response = send(json.dumps({"type": 1}), require_response=True)
      try:
          unjsoned_resp = json.loads(response)
          print(unjsoned_resp)
          watering.set_pins(unjsoned_resp)
      except TypeError as e:
          print(f"Response not recieved: ({e})")
      counter += 1
      if counter == 360:
        # one in 360 cyrcles measures data and send them to server
        counter = 0
      gc.collect()
      sleep(5)
        
   
   
main()


