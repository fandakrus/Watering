from machine import Pin, time_pulse_us



p = Pin(14, Pin.IN, Pin.PULL_DOWN)
print(p.value())

