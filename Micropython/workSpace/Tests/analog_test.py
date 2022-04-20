from machine import ADC, Pin
from time import sleep

while True:
    adc = ADC(Pin(34))
    adc.atten(ADC.ATTN_11DB)
    print(adc.read())
    sleep(3) 