from bluetooth import *
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

    # oled.set_cursor(2, 5) 
    # oled.print('BT:')

    # set cursor position
    oled.set_cursor(35-(len(message)*5), 20) 
    oled.print(message)

    # display screen
    oled.display()

def oled_print_speed(data):
    # clear the screen
    oled.clear(oled.PAGE)
    oled.display()

    # set the font size
    oled.set_font_type(1)

    # oled.set_cursor(2, 5) 
    # oled.print('BT:')

    # set cursor position
    oled.set_cursor(35-(len(data[0])*5), 20) 
    oled.print(data[0])

    # set cursor position
    oled.set_cursor(35-(len(data[0])*5), 35) 
    oled.print(data[1])

    # display screen
    oled.display()

def oled_print_list(words):
    for word in words:
        oled_print(word)
        time.sleep(0.5)

print('Ready')
oled_print('Ready')

server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",2))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

advertise_service( server_sock, "AquaPiServer", service_id = uuid, service_classes = [ uuid, SERIAL_PORT_CLASS ], profiles = [ SERIAL_PORT_PROFILE ],)

print('Advertised')
oled_print('Advertised')

def wait_for_connection():
    print ("Waiting for connection on RFCOMM channel", port)
    oled_print('Waiting')
    client_sock, client_info = server_sock.accept()
    print ("Accepted connection from ", client_info)
    oled_print('Connected')
    return client_sock, client_info
    
connected = False

while True:
    try:
        if not connected:
            client_sock, client_info = wait_for_connection()
            connected = True
        data = client_sock.recv(1024)
        print ("Phone sent:", str(data))
        message = str(data, 'utf-8')
        if '|' in message:
            oled_print_speed(message.split('|'))
        else:
            oled_print_list(message.split())
        data = "RPI received: " + str(data)
        client_sock.send(data)
        print ("Sent to Phone: [", data, "]")
    except IOError:
        pass
        print ("device terminated connection")
        oled_print('Terminated')
        connected = False
    except KeyboardInterrupt:
        oled_print('')
        print ("disconnected by user")
        if connected:
            client_sock.close()
            server_sock.close()
            print ("socket closed")
        break