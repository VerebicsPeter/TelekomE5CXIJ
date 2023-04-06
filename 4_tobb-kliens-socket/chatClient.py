import socket
import sys
from input_timeout import readInput

username = sys.argv[1]

def prompt(nl):
	if nl:
		print('')
	print('<'+username+'> ', end='')
	sys.stdout.flush()

print('Type \'exit\' to quit from chat.')

server_addr = ('localhost',10000)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
	
	client.connect(server_addr)
	client.sendall(username.encode())
	client.settimeout(1.0)
	prompt(False)
	
	while True:
		try:
			data = client.recv(4096)
			if not data:
				print("Server down")
			else:
				print(data.decode())
				sys.stdout.flush()
				prompt(False)
		except:
			pass
		try:
			msg = readInput()
			if msg == 'exit':
				exit(0)
			elif msg != '':
				msg = msg.strip()
				client.sendall(msg.encode())
				prompt(True)
		except SystemExit:
			client.close()
			exit(0)

# azert ilyen nem lesz a ZH-n