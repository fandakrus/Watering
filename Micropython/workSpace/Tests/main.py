import machine
from time import sleep

LED = machine.Pin(2, machine.Pin.OUT)
print(LED.value())
while True:
    LED.value(1)
    sleep(3)
    LED.value(0)
    sleep(4)
    