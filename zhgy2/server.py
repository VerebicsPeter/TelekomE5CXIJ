import sys
import struct
from socket import socket, AF_INET, SOCK_STREAM, timeout, SOL_SOCKET, SO_REUSEADDR
from select import select
import random

nums = []

def gen_numbers():
	for i in range(0,5):
		num = random.randint(1, 20)
		while (num in nums):
			num = random.randint(1, 20)
		nums.append(num)
	print(nums)

print('Generating numbers.'); gen_numbers()
server_addr = ('localhost', 10000)
packer = struct.Struct('I I I I I I') # last int is the bet
print('Starting server.')

with socket(AF_INET, SOCK_STREAM) as server:
	server.bind(server_addr)
	server.listen(1)
	server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	print('Server is listening on port', server_addr[1])
	
	sockets = [ server ]

	while True:
		r,w,e = select(sockets,[],[],1)
		# check if one of the lists is empty
		if not (r or w or e): continue
		
		for s in r:
			if s is server:
				# client connects
				client, client_addr = s.accept()
				sockets.append(client)
				print("Connected:", client_addr)

			else:
				data = s.recv(packer.size)
				
				# client disconnected if 0 bytes is sent
				if not data:
					sockets.remove(s); s.close()
					print('Client disconnected.')
				else:
					print('Recieved:', data)
					unp_data = packer.unpack(data)
					print('Unpack:', unp_data)

					matches = 0
					for i in range(0, 5):
						if (unp_data[i] in nums): matches+=1
					
					print('Matches:', matches)
					
					res = (nums[0], nums[1], nums[2], nums[3], nums[4], matches * unp_data[5])
					packed_res = packer.pack(*res)
					s.sendall(packed_res)