from machine import ADC, Pin
from time import ticks_diff, ticks_ms

lightsensor = ADC(Pin(39))

btn = Pin(34, Pin.IN, Pin.PULL_UP) 
DEBOUNCE_MS = 200
last_press = 0

pressed_flag = False

def button_handler(pin):
    global last_press
    global pressed_flag
    now = ticks_ms()
    if ticks_diff(now, last_press) > DEBOUNCE_MS:
        if (pin.value() == 0):
            last_press = now
            pressed_flag = True

btn.irq(trigger=Pin.IRQ_FALLING, handler=button_handler)

while True:
    if pressed_flag:
        print(lightsensor.read_u16())
        pressed_flag = False