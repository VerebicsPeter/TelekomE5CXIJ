from socket import socket, AF_INET, SOCK_DGRAM, timeout, SOL_SOCKET, SO_REUSEADDR
import struct

server_addr = ('localhost', 10002)
packer = struct.Struct('128s') # string of length 128

with socket(AF_INET, SOCK_DGRAM) as client:
	client.connect(server_addr)
	x = input("x: ")
	y = input("y: ")
	h = input("h: ")
	m = input("m: ")
	
	message = x + ';' + y + ';' + h + ';' + m + ";E5CXIJ"
	print(message)
	# pack message
	packed_data = packer.pack(message.encode())
	# send message
	client.sendall(packed_data)
	# recieve response
	data = client.recv(128).decode()
	print("Result:", data)
