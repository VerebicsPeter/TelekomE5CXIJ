from socket import socket, AF_INET, SOCK_DGRAM, timeout
import struct

packer = struct.Struct("I I 1s")

s1 = input("Szam1:")
o  = input("Operator:")
s2 = input("Szam2:")

values = (int(s1),int(s2),o.encode())

packed_data = packer.pack(*values)

with socket(AF_INET, SOCK_DGRAM) as client:
	server_address = ('localhost',10000)
	
	client.sendto(packed_data,server_address)
	
	data, _ = client.recvfrom(1024)
	
	print("Kaptam: ",data.decode())
