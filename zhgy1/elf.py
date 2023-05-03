import struct, time
from socket import socket, AF_INET, SOCK_STREAM, timeout, SOL_SOCKET, SO_REUSEADDR

server_addr = ('localhost', 10000)
packer = struct.Struct('128s I') # char[1], int

def get_and_send_packet(client):
	packet = input('Packet: ')
	weight = input('Weight: ')
	packed_data = packer.pack(packet.encode(), int(weight))
	client.sendall(packed_data)

with socket(AF_INET, SOCK_STREAM) as client:
	client.connect(server_addr)

	get_and_send_packet(client)
	data = client.recv(128).decode()
	print('answer:', data)

	while True:
		get_and_send_packet(client)
		data = client.recv(128).decode()
		print('answer:', data)
		if (data == 'TELE'): time.sleep(5)
