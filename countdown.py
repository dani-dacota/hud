import qwiic
import time

# Define oled screen and initialize
oled = qwiic.QwiicMicroOled()
oled.begin()
    
def oled_print(message):
    # clear the screen
    oled.clear(oled.PAGE)
    oled.display()

    # set the font size
    oled.set_font_type(1)

    oled.set_cursor(2, 5) 
    oled.print(message)

    # display screen
    oled.display()

for i in range(30):
    oled_print('-'+str(30-i)+'-')
    time.sleep(1)

oled_print('-X-')