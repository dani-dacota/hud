"""
A simple Python script to receive messages from a client over
Bluetooth using Python sockets (with Python 3.3 or above).
"""

import socket
import qwiic

def display(x, y, message):
    oled.clear(oled.PAGE)
    oled.set_cursor(x, y)
    oled.print(message)
    oled.display()



if __name__ == "__main__":
    # Define oled screen and initialize
    oled = qwiic.QwiicMicroOled()
    oled.begin()

    # clear the screen
    oled.clear(oled.PAGE)
    oled.display()

    # set the font size
    oled.set_font_type(1)

    print("Waiting to receive BT data")

    # The MAC address of a Bluetooth adapter on the server
    hostMACAddress = 'B8:27:EB:3A:A3:33' 

    # 3 is arbitrary but must match the port used by the client
    port = 3 

    # similar to queue depth
    backlog = 1

    #block size in bytes
    size = 1024

    s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    s.bind((hostMACAddress,port))
    s.listen(backlog)

    # set cursor position
    display(5,5,'BT')

    try:
        client, address = s.accept()
        while True:
            data = client.recv(size)
            if data:
                print(data)
                display(5,5, str(data))
                client.send(data)
    except:	
        print('Closing socket')	
        display(5,5, 'Error')
        client.close()
        s.close()