from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, timeout
from select import select
import struct

server_addr = ('', 10000)
unpacker = struct.Struct('I I 1s') # int, int, char[1]

with socket(AF_INET, SOCK_STREAM) as server:
	server.bind(server_addr)
	server.listen(1)
	server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	
	socketek = [ server ]
	
	while True:
		r,w,e = select(socketek,[],[],1)
		
		if not (r or w or e): # check if one of the lists is empty
			continue
		
		for s in r:
			if s is server:
				# kliens csatlakozik
				client, client_addr = s.accept()
				socketek.append(client)
				print("Csatlakozott", client_addr)
			else:
				data = s.recv(unpacker.size)
				# ha 0 byte akkor kilepett a kliens
				if not data:
					socketek.remove(s)
					s.close()
					print("Kilepett")
				else:
					print("Kaptam:", data)
					unpacked_data = unpacker.unpack(data)
					print("Unpack:", unpacked_data)
					x = eval(str(unpacked_data[0])+unpacked_data[2].decode()+str(unpacked_data[1]))
					print("Kiértékeltem és visszaküldtem", x)
					s.sendall(str(x).encode())