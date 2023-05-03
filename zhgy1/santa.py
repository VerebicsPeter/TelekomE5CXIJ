import struct, time
from socket import socket, AF_INET, SOCK_STREAM, timeout, SOL_SOCKET, SO_REUSEADDR

server_addr = ('localhost', 10000)
packer = struct.Struct('128s I') # char[1], int

with socket(AF_INET, SOCK_STREAM) as client:
	client.connect(server_addr)

	while True:
		print('sleeping 1s')
		time.sleep(1)
		packed_data = packer.pack(b'', 0)
		client.sendall(packed_data)
		data = client.recv(128).decode()
		print('answer:', data)
		if data == 'TELE':
			packed_data = packer.pack(b'elindultam', 0)
			client.sendall(packed_data)
			data = client.recv(128).decode()
			time.sleep(5)
