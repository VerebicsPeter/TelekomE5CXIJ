import socket
import sys

TCP_IP = 'localhost'	#sys.argv[1]
TCP_PORT = 10000		#int(sys.argv[2])
BUFFER_SIZE = 1024
message = b'Hello server!'

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((TCP_IP, TCP_PORT))
sock.send(message)
reply = sock.recv(BUFFER_SIZE)
sock.close()

print("Kapott válasz:", reply.decode())