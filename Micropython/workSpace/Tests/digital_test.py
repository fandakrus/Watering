from machine import Pin

p2 = Pin(5, Pin.IN, Pin.PULL_DOWN)
print(p2.value())