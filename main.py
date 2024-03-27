from machine import Pin, PWM, RTC
from math import floor
from time import sleep_ms, gmtime, time
import ntptime
pinDigit=[3,5,12,14]
pinData=[15,13,16,1]
pinLE=0
pinDots=4
offset=1*60*60 # Timezone offset in seconds
dstOffset=1*60*60 # additional Daylight Saving Time offset in seconds
digits=[Pin(pinDigit[0],Pin.OUT,value=0),Pin(pinDigit[1],Pin.OUT,value=0),Pin(pinDigit[2],Pin.OUT,value=0),Pin(pinDigit[3],Pin.OUT,value=0)]
datas= [Pin(pinData[0], Pin.OUT,value=0),Pin(pinData[1], Pin.OUT,value=0),Pin(pinData[2], Pin.OUT,value=0),Pin(pinData[3], Pin.OUT,value=0)]
dots=PWM(Pin(4,Pin.OUT))
dotsDuty=100 #dutycycle on the Dots, adjust to balance with LEDs Brightness
latch=Pin(0,Pin.OUT,value=1)
numberDelay = [9, 3, 8, 8, 6, 7, 7, 4, 9, 8];
rtc = RTC()

def setDigit(digit, number):
    for pin in range(4):
        datas[pin].value(1 if number & (1 << pin) else 0)
    for pin in range(4):
        digits[pin].value(1)
    latch.value(0)
    digits[digit].value(0)
    latch.value(1)
    sleep_ms(numberDelay[number])
    
def start():
    dst=0
    stamp=[0,0,0,0,0,0,0,0]
    oldStamp=[-1,-1,-1,-1,-1,-1]
    lastcheck=0
    while True:
        if oldStamp[4] != stamp[4]:
            oldHour=oldStamp[3]
            oldStamp=stamp
            try:
                if time() - lastcheck > 6:
                    ntptime.settime()
                    lastcheck=time()
            except:
                pass
            stamp=gmtime(time()+offset+dst)
            if oldHour != stamp[3]:
                ###
                # Do a DST verification, for CET: From last Sunday of March until last Sunday of October
                # DST Calculation, should add 1hour during these conditions
                # based on no-dst time (x)
                # months Apr-Sep
                # month March, after final sunday
                # month October, before final sunday (monthday - weekday < 26)
                # month March, on final sunday time after 2AM
                # month October, on final sunday time before 2AM
                ###
                baseStamp=gmtime(time()+offset)
                if  ( baseStamp[1] > 3 and baseStamp[1] < 10 ) or \
                    ( baseStamp[1]==3 and baseStamp[6] > 6 and baseStamp[2]-baseStamp[6] > 25 ) or \
                    ( baseStamp[1]==3 and baseStamp[6]==6 and baseStamp[2] > 25 and baseStamp[3] >= 2 ) or \
                    ( baseStamp[1]==10 and baseStamp[6] > 6 and baseStamp[2]-baseStamp[6] < 25) or \
                    ( baseStamp[1]==10 and baseStamp[6]==6 and baseStamp[2] > 25 and baseStamp[3] < 2 ):
                    dst=dstOffset
                else:
                    dst=0
            print(str(stamp[3]) + ":" + str(stamp[4]), dst)
        else:
            stamp=gmtime(time()+offset+dst)
        setDigit(0,floor(stamp[3]/10))
        setDigit(1,floor(stamp[3]%10))
        setDigit(2,floor(stamp[4]/10))
        setDigit(3,floor(stamp[4]%10))
        dots.duty(dotsDuty if (stamp[5]%2) else 0)

sleep_ms(2500)
while True:
    start()
