from socket import socket, AF_INET, SOCK_STREAM
import sys

server_addr = ('localhost', 10000)

if len(sys.argv) > 1:
    file = sys.argv[1]
else:
    file = "output.txt"

with socket(AF_INET,SOCK_STREAM) as server:
	server.bind(server_addr)
	server.listen(1)
	
	client, client_addr = server.accept()
	end = False
	with open(file, "wb") as f: #bináris módban nyitjuk meg
		while not end:
			data = client.recv(10)
			if data:
				f.write(data)
			else:
				client.close()
				end = True
print("Sikerult")