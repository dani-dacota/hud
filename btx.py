"""
A simple Python script to receive messages from a client over
Bluetooth using Python sockets (with Python 3.3 or above).
"""

import socket


if __name__ == "__main__":
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

    try:
        client, address = s.accept()
        while True:
            data = client.recv(size)
            if data:
                print(data)
                client.send(data)
    except:	
        print('Closing socket')	
        client.close()
        s.close()