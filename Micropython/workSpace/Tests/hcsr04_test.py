from hcsr04 import HCSR04
from time import sleep

# connects sensor with trig pin on GPI12 and echo pin on GPIO14
# timeout set to 20000 for longer distances measurement
sensor = HCSR04(trigger_pin=12, echo_pin=14, echo_timeout_us=20000)

distance = sensor.distance_cm()
print("Distance: ", distance , " cm")