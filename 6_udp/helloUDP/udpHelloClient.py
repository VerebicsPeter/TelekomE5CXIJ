from socket import socket, AF_INET, SOCK_DGRAM, timeout

with socket(AF_INET, SOCK_DGRAM) as client:
	server_address = ('localhost',10000)
	
	client.sendto("Hello Server".encode(),server_address)
	
	data, _ = client.recvfrom(1024)
	
	print("Kaptam: ",data.decode())
