
#socket_multicast_receiver.py

import socket
import struct
import sys
from socket import timeout

multicast_group = '224.3.29.71'
server_address = ('', 10000)

# Create the socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to the server address
sock.bind(server_address)

# Tell the operating system to add the socket to
# the multicast group on all interfaces.
group = socket.inet_aton(multicast_group)   #IP address to packed format
mreq = struct.pack('4sL', group, socket.INADDR_ANY)
sock.setsockopt(
    socket.IPPROTO_IP,
    socket.IP_ADD_MEMBERSHIP,
    mreq)

sock.settimeout(5.0)

# Receive/respond loop
while True:
    try:
        print('\nwaiting to receive message')
        data, address = sock.recvfrom(1024)
        
        print('received {} bytes from {}'.format(
            len(data), address))
        print(data)
        
        print('sending acknowledgement to', address)
        sock.sendto(b'ack', address)
    except timeout:
        pass

