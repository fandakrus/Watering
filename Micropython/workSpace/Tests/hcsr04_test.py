from hcsr04_lib import HCSR04
from time import sleep

# connects sensor with trig pin on GPI12 and echo pin on GPIO14
# timeout set to 20000 for longer distances measurement
sensor = HCSR04(trigger_pin=12, echo_pin=14, echo_timeout_us=40000)

for i in range(5):
    distance = sensor.distance_cm()
    print("Distance: ", distance , " cm")
    sleep(1)