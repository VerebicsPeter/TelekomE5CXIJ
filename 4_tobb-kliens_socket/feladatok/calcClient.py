from socket import socket, AF_INET, SOCK_STREAM, timeout, SOL_SOCKET, SO_REUSEADDR
import struct
import random
import time

server_addr = ('localhost', 10000)
packer = struct.Struct('I I 1s') # int, int, char[1]

with socket(AF_INET, SOCK_STREAM) as client:
	client.connect(server_addr)
	for i in range(10) :
		time.sleep(2)

		print('\n(', i, ') művelet:\n')

		szam1 = random.randint(1, 100) # input("Adj meg egy szamot:")
		szam2 = random.randint(1, 100) # input("Adj meg masik szamot:")
		op = input("Adj meg egy operátort:") # esetleg ezt is lehet randomizálni

		values = (int(szam1), int(szam2), op.encode())
		packed_data = packer.pack(*values)
		
		client.sendall(packed_data)
		data = client.recv(10).decode()
	
		print("Eredmény:", data)
# close socket