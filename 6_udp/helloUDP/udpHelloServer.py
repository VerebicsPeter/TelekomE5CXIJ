from socket import socket, AF_INET, SOCK_DGRAM, timeout

with socket(AF_INET, SOCK_DGRAM) as server:
	server_address = ('localhost',10000)
	
	server.bind(server_address)
	server.settimeout(1.0)
	
	while True:
		try:
			data, client = server.recvfrom(1024)

			print("Kaptam", data.decode(),"tole:",client)

			server.sendto("Hello kliens!".encode(), client)
		except timeout:
			pass