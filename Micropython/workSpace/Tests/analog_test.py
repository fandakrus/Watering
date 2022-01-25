from machine import ADC, Pin
from time import sleep

while true:
    adc = ADC(Pin(36))
    adc.atten(ADC.ATTN_11DB)
    print(adc.read())
    sleep(3)