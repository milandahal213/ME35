import network
import espnow
import time
import json

import neopixel
from machine import Pin
np = neopixel.NeoPixel(Pin(15),2)


# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.WLAN.IF_STA)
sta.active(True)
sta.disconnect()   # Because ESP8266 auto-connects to last Access Point

e = espnow.ESPNow()
e.active(True)

mac_addresses = []
message = b''
macadd = b''
new_message = False

def recv_cb(esp):
    global message, macadd, new_message
    if esp.any():
        mac, msg = esp.irecv(0)  # Read immediate message buffer
        if mac is not None:
            #print(mac, msg)
            message = msg
            macadd = mac
            new_message = True
            
            
e.irq(recv_cb)

while True:
    if new_message:
        print(message, macadd)
        state = json.loads(message)["state"]
        color = json.loads(message)["color"]
        if state == "normal":
            pass
        elif state == "green":
            np[0] = color
            np.write()
        elif state == "red":
            np[0] = color
            np.write()
        print(color)
        new_message = False
    time.sleep(1)
    



