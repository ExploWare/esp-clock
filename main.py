from machine import Pin, PWM, RTC
from math import floor
from time import sleep_ms, gmtime, time
import ntptime
pinDigit=[3,5,12,14]
pinData=[15,13,16,1]
pinLE=0
pinDots=4
offset=3600
digits=[Pin(pinDigit[0],Pin.OUT,value=0),Pin(pinDigit[1],Pin.OUT,value=0),Pin(pinDigit[2],Pin.OUT,value=0),Pin(pinDigit[3],Pin.OUT,value=0)]
datas= [Pin(pinData[0], Pin.OUT,value=0),Pin(pinData[1], Pin.OUT,value=0),Pin(pinData[2], Pin.OUT,value=0),Pin(pinData[3], Pin.OUT,value=0)]
dots=PWM(Pin(4,Pin.OUT))
latch=Pin(0,Pin.OUT,value=1)
numberDelay = [1, 5, 1, 1, 3, 2, 2, 5, 0, 2];
rtc = RTC()
verifier = -1
def setDigit(digit, number):
    for pin in range(4):
        datas[pin].value(1 if number & (1 << pin) else 0)
    for pin in range(4):
        digits[pin].value(1)
    latch.value(0)
    digits[digit].value(0)
    latch.value(1)
    sleep_ms(floor((9-numberDelay[number])));

    
def start():
    dst=0
    stamp=[0,0,0,0,0,0,0,0]
    oldStamp=[-1,-1,-1,-1,-1,-1]
    while True:
        if oldStamp[4] != stamp[4]:
            oldHour=oldStamp[3]
            oldStamp=stamp
            try:
                ntptime.settime()
            except:
                pass
            stamp=gmtime(time()+offset+dst)
            if oldHour != stamp[3]:
                ### Do a DST verification.
                ### DST Calculation, should add 1hour during these conditions
                # based on no-dst time (x)
                # months Apr-Sep
                # month March, after final sunday
                # month October, before final sunday (monthday - weekday < 25)
                # month March, on final sunday time after 2AM
                # month October, on final sunday time before 2AM
                baseStamp=gmtime(time()+offset)
                if  ( baseStamp[1] > 3 and baseStamp[1] < 10 ) or \
                    ( baseStamp[1]==3 and baseStamp[6]<6 and baseStamp[2] > 25) or \
                    ( baseStamp[1]==10 and baseStamp[2]-baseStamp[6] < 25) or \
                    ( baseStamp[1]==3 and baseStamp[6]==6 and baseStamp[2] > 24 and baseStamp[3] >= 2 ) or \
                    ( baseStamp[1]==10 and baseStamp[6]==6 and baseStamp[2] > 24 and baseStamp[3] >= 2 ):
                    dst=3600
                else:
                    dst=0
        else:
            stamp=gmtime(time()+offset+dst)
        setDigit(0,floor(stamp[3]/10))
        setDigit(1,floor(stamp[3]%10))
        setDigit(2,floor(stamp[4]/10))
        setDigit(3,floor(stamp[4]%10))
        dots.duty(100 if (stamp[5]%2) else 0)
        
def sync():
        try:
            t=time.localtime(ntptime.time()+3600)                                                                                                             
            rtc.datetime([t[0],t[1],t[2],0,t[3],t[4],t[5],0])                                                                                                 
        except:
            pass

sleep_ms(1500)
while True:
    start()
