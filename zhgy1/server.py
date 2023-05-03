from socket import socket, AF_INET, SOCK_STREAM, timeout, SOL_SOCKET, SO_REUSEADDR
from select import select
import struct

weight = 0

server_addr = ('localhost', 10000)
unpacker = struct.Struct('128s I') # char[128], int

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
				# kliens csatlakozik
				client, client_addr = s.accept()
				sockets.append(client)
				print("Connected:", client_addr)
			else:
				data = s.recv(unpacker.size)
				# ha 0 byte akkor kilepett a kliens
				if not data:
					sockets.remove(s)
					s.close()
					print("Left.")
				else:
					print("Recieved:", data)
					santa_started = unpacker.pack(b'elindultam', 0)
					if data == santa_started: weight = 0

					unp_data = unpacker.unpack(data)
					
					print("Unpacked weight:", unp_data[1])
					print("Total weight:", weight)
					
					weight += unp_data[1]
					if weight >= 15: s.sendall(b"TELE")
					else: s.sendall(b"OK")

# ZH-n is lehet ezt a szerkezetet hasznalni