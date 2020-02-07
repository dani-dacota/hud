from bluetooth import *

server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

advertise_service( server_sock, "AquaPiServer", service_id = uuid, service_classes = [ uuid, SERIAL_PORT_CLASS ], profiles = [ SERIAL_PORT_PROFILE ],)
while True:
    print ("Waiting for connection on RFCOMM channel", port)
    client_sock, client_info = server_sock.accept()
    print ("Accepted connection from ", client_info)
    try:
        data = client_sock.recv(1024)
        print ("Phone sent", data)
        data = "RPI received" +  data 
        client_sock.send(data)
        print ("Sent to Phone", data)
    except IOError:
        pass
    except KeyboardInterrupt:
        print ("disconnected by user")
    except:
        client_sock.close()
        server_sock.close()
        print ("all done")