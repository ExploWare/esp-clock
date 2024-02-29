import gc
import utime
gc.collect()
time_start=utime.ticks_ms()
from secrets import secrets
# This file is executed on every boot (including wake-boot from deepsleep)

#Get out of the UART with mismatched baudrate on the serial
print('        '*40+'\n')
print('boot.py')

connection_timeout = 18
known_accesspoints=[secrets['known_wifi']] #list of lists as [['ssid','wpa-psk']]
from time import sleep
import network
import esp
esp.osdebug(None)
import os
os.dupterm(None, 1)

#initiate wifi, done after the callback is set up
wlan = network.WLAN(network.STA_IF)
counter=0

while not wlan.isconnected():
    sleep(1)
    counter +=1
    if counter > connection_timeout:
        break
while not wlan.isconnected():
    accesspoints=sorted(wlan.scan(), key=lambda sig_str: -sig_str[3])
    for accesspoint in accesspoints:
        print('try:'+accesspoint[0].decode())
        if accesspoint[0].decode() in str(known_accesspoints):
            for known_accesspoint in known_accesspoints:
                if accesspoint[0].decode() == known_accesspoint[0]:
                    break
            counter=0
            print('trying '+accesspoint[0].decode() )
            wlan.connect(known_accesspoint[0],known_accesspoint[1])
            while not wlan.isconnected():
                print("waiting for manual connection:"+str(connection_timeout-counter)+"Seconds")
                counter +=1
                sleep(1)
                if counter > connection_timeout:
                    print("could not connect to " + known_accesspoint[0])
                    ap = network.WLAN(network.AP_IF) # create access-point interface
                    ap.active(True)         # activate the interface
                    ap.config(ssid=secrets['accesspoint']['ssid'], password=secrets['accesspoint']['ssid']) # set the SSID of the access point
                    break
                pass
            break

if(wlan.isconnected()):
    print("connected!:")
    print(str(wlan.ifconfig()))
    ap = network.WLAN(network.AP_IF) # create access-point interface
    ap.active(False)
else:
    try:
        print("Connectable:")
        print(str(ap.config('ssid')))
    except:
        ap = network.WLAN(network.AP_IF) # create access-point interface
        ap.active(True)         # activate the interface
        ap.config(ssid=secrets['accesspoint']['ssid'], password=secrets['accesspoint']['ssid']) # set the SSID of the access point
        print(str(ap.config('ssid')))
    finally:
        print(str(ap.ifconfig()))

import webrepl
webrepl.start()