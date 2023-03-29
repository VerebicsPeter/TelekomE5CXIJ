import socket
import select
import queue
import struct

server_addr = ('',10000)
packer = struct.Struct('I I 1s')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
	server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server.bind(server_addr)
	server.listen(5)
	
	sockets = [ server ]		
	
	msg_queue = queue.Queue()
	username = {}
	
	while True:
		r, w, e = select.select(sockets,sockets,sockets,1)

		if not (w or r or e):
			continue
		
		for s in r:
			if s is server:
				#Ha szerver
				client, client_addr = s.accept()
				client.setblocking(0)
				
				name = client.recv(20).decode()
				print("Csatlakozott: ",name.strip(),client_addr)
				
				username[client] = name.strip()
				msg_queue.put( (client, "["+name+"] -LOGIN-") )
				
				sockets.append(client)
			else:
				#Ha nem szerver
				data = s.recv(1024)
				if not data:
					sockets.remove(s)
					if s in w:
						w.remove(s)
					s.close()
					msg_queue.put ( (s, "["+username[s]+"] -LOGOUT-") )
				else:
					msg_queue.put( (s, "["+username[s]+"] "+data.decode().strip()) )
		
		while not msg_queue.empty():
			try:
				(client, msg) = msg_queue.get_nowait() #Ha üres a queue, akkor tovább lép
			except queue.Empty:
				break
			else:
				for s in w:
					if not s is client:
						s.sendall(msg.encode())

# azert ilyen nem lesz a ZH-n