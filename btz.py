from bluetooth import *




server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",2))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

advertise_service( server_sock, "AquaPiServer", service_id = uuid, service_classes = [ uuid, SERIAL_PORT_CLASS ], profiles = [ SERIAL_PORT_PROFILE ],)

def wait_for_connection():
    print "Waiting for connection on RFCOMM channel", port
    client_sock, client_info = server_sock.accept()
    print "Accepted connection from ", client_info

wait_for_connection()

while True:
    try:
        data = client_sock.recv(1024)
        print "Phone sent", data
        data = "RPI received " +  data 
        client_sock.send(data)
        print "Sent to Phone", data
    except IOError:
        pass
        print "device terminated connection"
        wait_for_connection()
    except KeyboardInterrupt:
        print "disconnected by user"
        client_sock.close()
        server_sock.close()
        print "all done"
        break