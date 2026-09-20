from machine import ADC, Pin
import time
lightsensor = ADC(Pin(39))
print(lightsensor.read_u16())


    
        