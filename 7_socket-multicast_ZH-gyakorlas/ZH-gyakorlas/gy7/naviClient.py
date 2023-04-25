from socket import socket, AF_INET, SOCK_STREAM, timeout, SOL_SOCKET, SO_REUSEADDR
import struct

server_addr = ('localhost', 10000)
packer = struct.Struct('128s') # string of length 128

with socket(AF_INET, SOCK_STREAM) as client:
	client.connect(server_addr)
	x = input("x: ")
	y = input("y: ")
	h = input("hour: ")
	m = input("minute: ")
	
	message = x + ';' + y + ';' + h + ';' + m + ";E5CXIJ"
	print(message)
	# pack message
	
	#client.sendall(packed_data)
	#data = client.recv(10).decode()
	
	#print("Eredmeny:", data)