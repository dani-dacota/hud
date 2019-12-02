#! /usr/bin/python3

from __future__ import print_function
from datetime import datetime
import qwiic_py
import qwiic
import time
import sys


# Define oled screen and initialize
oled = qwiic.QwiicMicroOled()
oled.begin()

# clear the screen
oled.clear(oled.PAGE)
oled.display()

# set the font size
oled.set_font_type(1)

while True:

    now = datetime.now()
    currentTime = now.strftime("%H:%M")

    # set cursor position
    oled.set_cursor(10, 8)  # top left of screen
    oled.print("Hello")

    # oled.set_cursor(0,22)
    # oled.print("TA!")
    oled.set_cursor(10, 20)
    oled.print(currentTime)

    # display screen
    oled.display()

    time.sleep(.5)
    oled.clear(oled.PAGE)
