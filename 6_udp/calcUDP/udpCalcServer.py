from socket import socket, AF_INET, SOCK_DGRAM, timeout
import struct

packer = struct.Struct("I I 1s")

with socket(AF_INET, SOCK_DGRAM) as server:
	server_address = ('localhost',10000)
	
	server.bind(server_address)
	server.settimeout(1.0)
	
	while True:
		try:
			data, client = server.recvfrom(packer.size)
			
			unpacked_data = packer.unpack(data)

			print("Kaptam", unpacked_data,"tole:",client)
			
			x = eval(str(unpacked_data[0])+unpacked_data[2].decode()+str(unpacked_data[1]))

			server.sendto(str(x).encode(), client)
		except timeout:
			pass