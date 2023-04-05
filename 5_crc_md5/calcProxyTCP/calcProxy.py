from socket import socket, AF_INET, SOCK_STREAM
import select, struct

proxy_addr = ('localhost',10000)
server_addr = ('localhost',11000)

packer = struct.Struct('i i c')

def sabotage(original):
	sabotageData = list(packer.unpack(original))
	print("Eredeti üzenete:",sabotageData)
	sabotageData[0] = sabotageData[0]*2
	sabotageData[1] = sabotageData[1]+1
	print("Szabotált üzenete:",sabotageData)
	reply = packer.pack(*tuple(sabotageData))
	return reply


with socket(AF_INET, SOCK_STREAM) as proxy, socket(AF_INET,SOCK_STREAM) as serverSock:
	proxy.bind(proxy_addr)
	proxy.listen(5)

	serverSock.connect(server_addr)

	
	
	inputs = [proxy]
	
	while True:
		r, w, e = select.select(inputs,inputs,inputs,1)
		
		if not (r or w or e):
			continue
		
		for s in r:
			if s is proxy:
				client, client_addr = s.accept()
				print("Kliens csatlakozott ",client_addr)
				inputs.append(client)
			else:
				data = s.recv(9)
				if not data:
					print("Kliens kilepett")
					inputs.remove(s)
					s.close()
				else:
					print("Szabotálás:")
					sData = sabotage(data)
					serverSock.sendto(sData,server_addr)
					respData, _ = serverSock.recvfrom(200)
					print("Szerver válasza:", respData)
					s.sendall(respData)