from socket import socket, AF_INET, SOCK_DGRAM, timeout
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

server_address = ('localhost',10001)
packer = struct.Struct("I I I I")

with socket(AF_INET, SOCK_DGRAM) as server:
	
	server.bind(server_address)
	server.settimeout(1.0)
	
	while True:
		try:
			data, client = server.recvfrom(packer.size)
			
			unpacked_data = packer.unpack(data)

			print("recieved:", unpacked_data, "from:", client)
			x, y, h, m = unpacked_data
			print("x =",x,"y =",y)
			print("@",h,":",m)
			
			res = search_map_data(x,y,h,m)
			res = str(res)
			server.sendto(res.encode(), client)
		except timeout:
			pass
