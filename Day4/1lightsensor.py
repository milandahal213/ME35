from machine import ADC, Pin
import time
lightsensor = ADC(Pin(25))
print(lightsensor.read_u16())


    
        