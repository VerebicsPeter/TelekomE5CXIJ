import sys
import socket
import struct

TCP_IP = 'localhost'	#sys.argv[1]
TCP_PORT = 10000		#int(sys.argv[2])
BUFFER_SIZE = 1024

operator = '-'
values = (1.1, operator.encode(), 2.7)
packer = struct.Struct('f 1s f')
packed_data = packer.pack(*values)

message = packed_data

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((TCP_IP, TCP_PORT))
sock.send(message)
reply = sock.recv(BUFFER_SIZE)
sock.close()

print("Kapott válasz:", reply.decode())

# szebb megoldas: calcClient