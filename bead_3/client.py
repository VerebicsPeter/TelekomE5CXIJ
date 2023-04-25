import sys
import struct
from socket import socket, AF_INET, SOCK_STREAM, timeout, SOL_SOCKET, SO_REUSEADDR

def logarithmic_search(min, max, client):
	center = (min + max) // 2 # number to check

	ceq = '=' # check for equality

	packed_data = packer.pack(ceq.encode(), int(center))
	client.sendall(packed_data)
	answer = client.recv(10).decode()

	if (answer[0] == 'Y'):
		print('Game won.')
		return # stop execution on win #

	cop = '<' # check recursively
	
	packed_data = packer.pack(cop.encode(), int(center))
	client.sendall(packed_data)
	answer = client.recv(10).decode()

	if (answer[0] == 'N'):
		logarithmic_search(center + 1, max, client)

	if (answer[0] == 'I'):
		logarithmic_search(min, center - 1, client)

	if (answer[0] == 'K'):
		print('Game lost.')
	
	if (answer[0] == 'V'):
		print('Game is over.')
	

if len(sys.argv) != 3:
	print('This program takes 2 arguments!')
	exit(1)

server_addr = (sys.argv[1], int(sys.argv[2]))
packer = struct.Struct('1s I') # char[1], int

with socket(AF_INET, SOCK_STREAM) as client:
	client.connect(server_addr)

	logarithmic_search(1, 100, client)

	# code for stdin below #
	"""
	cop = input('Comparison operator: ') # comparison operator
	num = input('Number: ')				 # number to compare
	
	packed_data = packer.pack(cop.encode(), int(num))
	
	client.sendall(packed_data)

	data = client.recv(10).decode()
	
	print('answer:', data[0])

	while data[0] == 'I' or data[0] == 'N' :
		cop = input('Comparison operator: ')
		num = input('Number: ')

		packed_data = packer.pack(cop.encode(), int(num))
		client.sendall(packed_data)

		data = client.recv(10).decode()
	
		print('answer:', data[0])
	"""