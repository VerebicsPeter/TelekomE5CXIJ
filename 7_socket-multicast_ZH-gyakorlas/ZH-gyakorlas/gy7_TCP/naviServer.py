from socket import socket, AF_INET, SOCK_STREAM, timeout, SOL_SOCKET, SO_REUSEADDR
from select import select
import struct

# proxy_addr is the proxy's address (client connects to this)
proxy_addr = ('localhost', 10000)
# mpbank_addr is the server address
mpbank_addr = ('localhost', 10001)

packer = struct.Struct('128s') # char[128]
mpbank_packer = struct.Struct('I I I I') # int, int, int, int

with socket(AF_INET, SOCK_STREAM) as proxy, socket(AF_INET,SOCK_STREAM) as server:
	proxy.bind(proxy_addr)
	proxy.listen(1)

	proxy.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	
	server.connect(mpbank_addr)
	
	sockets = [ proxy ]
	
	while True:
		r,w,e = select(sockets,[],[],1)
		
		if not (r or w or e): # check if one of the lists is empty
			continue
		
		for s in r:
			if s is proxy:
				# kliens csatlakozik
				client, client_addr = s.accept()
				print("Connected:", client_addr)
				sockets.append(client)
			else:
				data = s.recv(packer.size)
				# ha 0 byte akkor kilepett a kliens
				if not data:
					print("Client left.")
					sockets.remove(s)
					s.close()
				else:
					print("Recieved:", data)
					decoded_data = data.decode()
					print("Decoded data:", decoded_data)
					
					# send data without neptun code
					strings = decoded_data.split(';')
					to_send = mpbank_packer.pack(
						int(strings[0]),
						int(strings[1]),
						int(strings[2]),
						int(strings[3]))
					
					server.sendto(to_send, mpbank_addr)
					response = server.recvfrom(128)
					print("recieved:", response[0].decode())
					s.sendall(response[0])

# ZH-n is lehet ezt a szerkezetet hasznalni