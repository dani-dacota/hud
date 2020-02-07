from bluetooth import *
import qwiic

# Define oled screen and initialize
oled = qwiic.QwiicMicroOled()
oled.begin()

# clear the screen
oled.clear(oled.PAGE)
oled.display()

# set the font size
oled.set_font_type(1)

#setcursor on OLED
oled.set_cursor(2, 35)

#print to OLED
oled.write("BT")

#display screen
oled.display()

server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

advertise_service( server_sock, "AquaPiServer", service_id = uuid, service_classes = [ uuid, SERIAL_PORT_CLASS ], profiles = [ SERIAL_PORT_PROFILE ],)

print ("Waiting for connection on RFCOMM channel", port)
client_sock, client_info = server_sock.accept()
print ("Accepted connection from ", client_info)

while True:
    try:
        data = client_sock.recv(1024)
        print ("Phone sent", data)
        data = "RPI received " +  data 
        client_sock.send(data)
        print ("Sent to Phone", data)
    except IOError:
        pass
    except KeyboardInterrupt:
        print ("disconnected by user")
        break
    except:
        client_sock.close()
        server_sock.close()
        print ("all done")