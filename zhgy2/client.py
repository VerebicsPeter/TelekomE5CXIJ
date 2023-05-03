import struct
from socket import socket, AF_INET, SOCK_STREAM, timeout, SOL_SOCKET, SO_REUSEADDR

server_addr = ('localhost', 10000)
packer = struct.Struct('I I I I I I')

with socket(AF_INET, SOCK_STREAM) as client:
	client.connect(server_addr)

	num1 = input('Give me a guess between 1 and 20: ')
	num2 = input('Give me a guess between 1 and 20: ')
	num3 = input('Give me a guess between 1 and 20: ')
	num4 = input('Give me a guess between 1 and 20: ')
	num5 = input('Give me a guess between 1 and 20: ')
	bet = input('Give me your bet: ')
	
	packed_data = packer.pack(
			   int(num1),
			   int(num2),
			   int(num3),
			   int(num4),
			   int(num5),
			   int(bet))
	
	client.sendall(packed_data)

	data = client.recv(packer.size)
	print('recieved:', data)
	unpacked_data = packer.unpack(data)
	print('unpacked data:', unpacked_data)

	print('winning numbers:', unpacked_data[0:5])
	print('you won:', unpacked_data[5])