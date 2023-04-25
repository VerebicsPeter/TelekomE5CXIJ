import sys
import struct
from socket import socket, AF_INET, SOCK_STREAM, timeout, SOL_SOCKET, SO_REUSEADDR
from select import select
import random

if len(sys.argv) != 3:
	print('This program takes 2 arguments!')
	exit(1)

num = random.randint(1, 100) # random number to guess
print('number:', num)
guessed = False
guesses = {} # contains the number of guesses per client (client's adress)

server_addr = (sys.argv[1], int(sys.argv[2]))
unpacker = struct.Struct('1s I') # char[1], int

with socket(AF_INET, SOCK_STREAM) as server:
	server.bind(server_addr)
	server.listen(1)
	server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	
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
				guesses[client_addr] = 0
				print("Connected:", client_addr)

			else:
				data = s.recv(unpacker.size)
				
				# client disconnected if 0 bytes is sent
				if not data:
					sockets.remove(s)
					s.close()
					print('Client disconnected.')
				
				else:
					print('Recieved:', data)
					unp_data = unpacker.unpack(data)
					print('Unpack:', unp_data)
					operator, numstring = unp_data[0].decode(), str(unp_data[1])
					if operator == '=' : operator = '=='
					l = eval(str(num) + operator + numstring)

					msg = 0

					if guessed:
						msg = unpacker.pack(b'V', 0)
					elif guesses[s.getpeername()] >= 25:
						msg = unpacker.pack(b'K', 0)
					elif l:
						if operator == '==':				#
							guessed = True					# number is guessed
							msg = unpacker.pack(b'Y', 0)
						else:								#
							guesses[s.getpeername()] += 1	# guess is correct (but number isn't guessed)
							msg = unpacker.pack(b'I', 0)	
					else:									# 
						guesses[s.getpeername()] += 1		# guess isn't correct
						msg = unpacker.pack(b'N', 0)
					
					if (msg != 0): s.sendall(msg)
