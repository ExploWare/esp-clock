# esp-clock
## Simple 4x 7 segment clock, driven by ESP8266 and a 4511 BCDtoSevenSegment driver

## Why  
Because my television-box was replaced by a smaller box which did NOT have a clock, we had no visible time in the bedroom.  
Since I couldn't find any decent clock on the one day I've been looking for one, I decided to build one. Since I had a 4x7segment display and a esp12f module, I decided it will work.  
## How  
I started connecting my seven segment display onto an arduino to check and document the Anodes - Cathodes pairs.
Calculated 4 digits + 7 segments + one for the dots: 12 pins required  
The [ESP12F](https://docs.ai-thinker.com/_media/esp8266/docs/esp-12f_product_specification_en.pdf) module would expose 13 (counting the TX/RX as available GPIOs)
I know I wanted to work with [MicroPython](https://www.micropython.org) as it feels familiar to me. As it exposes a programming interface over Wifi (webrepl) I didn't need the UART interface.
But I miscounted, expecting all the exposed GPIO pins on the esp12f being available, but GPIO9 and 10 are in use for the on-board storage, and I do need that to work also.  
So I looked for a multiplexer / serial to parallel chip. I found some 7400 logic, and with some steps in between I found a 4000 series chip: [a HEF4511](https://www.learnabout-electronics.org/Downloads/HEF4511B.pdf), a BCD to Seven Segement latch driver.  
This reduced the required pins by 2 pins!  
Still, the ESP is completely full:  
- GPIO 1 and 3, normally the UART, are connected, I've skipped GPIO2 as it was connected to the blue LED on the ESP12F board, and I forgot to desolder it before soldering the board onto the perfboard.
- GPIO 15, 13, 16 an 1 are connected to the DATA pins of the 4511  
- GPIO0 to the Latch Enabled (This one allows the Pulled UP with a 10K resistor)  
The Blanking pin and the Light Test pin are pulled down to ground  
  
The 4x7 segment display has six common anodes:  
- one for each digit: GPIO 3, 5, 12 and 14, soldered with a 130 ohm resistor onto the ESP  
- two for the dots, I soldered these onto one pin: GPIO1  
the other two pins for the Dots are grounded while the segment pins of the display are directly soldered onto the 4511 outputs  
  
The new TV-box had a USB connector with power, I looked for a 3v3 regulator as the red LEDs of the display did work on 3v3 while testing on an arduino uno and the 4511 works on 3 to 15 volts.  
I did blow an LDO, probably missoldered my ground pin. So I desoldered one from an old webcam PCB.  
  
Visual for human it is not blinking, but in this nice slow motion recording, you can see the multiplexing  
(note the dots (colon) is directly addressed, and thus not multiplexed)  
![esp-clock-slomo gif](https://github.com/ExploWare/esp-clock/assets/6767397/2cced782-255e-4701-be2f-32a7e55fe456)  
  
  
Since the ESP8266 is really terrible at timekeeping (a drift of 6 minutes in the hour) and the clock only to be adjustable to 160MHz or 80MHz, there is need for a Real Time Clock. But I'm out of pins...
Luckely, the wifi of the ESP and the ntptime library being available in micropython, I was able to perform ntp requests. A lot. About every minute. No drift no mo
