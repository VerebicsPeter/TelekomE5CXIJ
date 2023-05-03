from socket import socket, AF_INET, SOCK_STREAM, timeout, SOL_SOCKET, SO_REUSEADDR
from select import select
import struct
import random

map_data = [{'location':(10,10),'h':10,'m':30,'t':69},
	    	{'location':(20,20),'h':20,'m':15,'t':20},
			{'location':(25,50),'h':12,'m':0 ,'t':15}]

def search_map_data(x,y,h,m):
	for elem in map_data:
		if elem['location'] == (x,y) and elem['h'] == h and elem['m'] == m:
			return elem['t']
	return random.randint(0, 100)

server_addr = ('localhost', 10001)
packer = struct.Struct('I I I I')

with socket(AF_INET, SOCK_STREAM) as server:
	server.bind(server_addr)
	server.listen(1)
	server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	
	sockets = [ server ]
	
	while True:
		r,w,e = select(sockets,[],[],1)
		
		if not (r or w or e): # check if one of the lists is empty
			continue
		
		for s in r:
			if s is server:
				client, client_addr = s.accept()
				print("Connected:", client_addr)
				sockets.append(client)
			else:
				data = s.recv(packer.size)
				if not data:
					print("Client left.")
					sockets.remove(s)
					s.close()
				else:
					print("Recieved:", data)
					unpacked_data = packer.unpack(data)
					print("Unpacked data:", unpacked_data)
					
					x , y , h, m = unpacked_data
					print("x =",x,"y =", y)
					print("@",h,":",m)
					res = search_map_data(x,y,h,m)
					res = str(res)
					s.sendall(res.encode())

# ZH-n is lehet ezt a szerkezetet hasznalni