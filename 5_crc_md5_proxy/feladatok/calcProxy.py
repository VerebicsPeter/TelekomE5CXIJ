import sys
from socket import socket,AF_INET, SOCK_STREAM
import select
import struct

packer = struct.Struct('I I 1s') # int, int, char[1]

proxy = socket(AF_INET, SOCK_STREAM)

proxy_addr  = ('', 10000)
server_addr = ('', 11000)

proxy.bind(proxy_addr); proxy.listen(10)
proxy.connect(server_addr)

inputs = [proxy]

while True:
	timeout = 1
	r, w, e = select.select(inputs,inputs,inputs,timeout)
	
	if not (r or w or e): continue
	
	for s in r:
		if s is proxy:
			print("Kliens csatlakozik ...")
			client, client_addr = s.accept()
			inputs.append(client)
		else:
			data = s.recv(65000)
			if not data:
				inputs.remove(s)
				s.close()
			else:
				data = s.recv(packer.size)
				# ha 0 byte akkor kilepett a kliens
				if not data:
					inputs.remove(s)
					s.close()
					print("Kilepett")
				else:
					print("Kaptam:", data)
					unp_data = packer.unpack(data)
					unp_data[0] *= 2
					unp_data[1] += 1
					data = packer.pack(*unp_data)
					proxy.send(data)
					print("proxy sent data")