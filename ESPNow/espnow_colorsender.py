import network
import espnow


# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.WLAN.IF_STA)  # Or network.WLAN.IF_AP
sta.active(True)
sta.disconnect()      # For ESP8266

e = espnow.ESPNow()
e.active(True)
peer = b'\xff\xff\xff\xff\xbb\xff'   # MAC address of peer's wifi interface
e.add_peer(peer)      # Must add_peer() before send()


import time
while True:
    e.send(peer,'{"color":[10,10,0]}')
    time.sleep(1)
    e.send(peer,'{"color":[0,10,0]}')
    time.sleep(1)
    e.send(peer,'{"color":[0,10,10]}')
    time.sleep(1)
    e.send(peer,'{"color":[010,0,10]}')
    time.sleep(1)

