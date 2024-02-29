# esp-clock
Simple 4x 7 segment clock, driven by ESP8266 and a 4511 BCDtoSevenSegment driver


An ESP12F was used with a HEF4511 chip for Binary Digits to Seven Segments, to save a few GPIO
the ESP is completely full:
GPIO 1 and 3, normally the UART, are connected, I've skipped GPIO2 as it was connected to the blue LED on the ESP12F board, and I forgot to desolder it before soldering the board onto the perfboard.
GPIO 15, 13, 16 an 1 are connected to the DATA pins of the 4511
GPIO0 to the Latch Enabled (This one allows the Pulled UP with a 10K resistor)
The Blanking pin and the Light Test pin are pulled down to ground
the 4x7 segment display has six common anodes:
- two for the dots, I soldered these onto one pin: GPIO1
- one for each digit: GPIO 3, 5, 12 and 14, soldered with a 130 ohm resistor onto the ESP
the other two pins for the Dots are grounded while the segment pins of the display are directly soldered onto the 4511 outputs

