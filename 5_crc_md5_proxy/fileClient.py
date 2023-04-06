from socket import socket, AF_INET, SOCK_STREAM
import sys

server_addr = ('localhost', 10000)

if len(sys.argv) > 1:
    file = sys.argv[1]
else:
    file = "input.txt"

with socket(AF_INET,SOCK_STREAM) as client:
	with open(file, "rb") as f: #bináris módban nyitjuk meg
		client.connect(server_addr)
		l = f.read(10)
		while l:
			client.sendall(l)
			l = f.read(10)
print("Elkuldtem")