import json
import struct
from socket import socket, AF_INET, SOCK_STREAM, timeout, SOL_SOCKET, SO_REUSEADDR
from select import select

json_dict = {}

with open('data.json', 'r') as json_file : json_dict = json.load(json_file)

if not json_dict: exit(1)

print('data:', json_dict)

server_addr = ('localhost', 10000)
packer = struct.Struct('I')

with socket(AF_INET, SOCK_STREAM) as server:
    server.bind(server_addr)
    server.listen(1)
    server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    print('Server started.')

    socketek = [ server ]
    
    while True:
        r,w,e = select(socketek,[],[],1)
        
        if not (r or w or e): continue
        
        for s in r:
            if s is server:
                # kliens csatlakozik
                client, client_addr = s.accept()
                socketek.append(client)
                print("Client connected:", client_addr)
            else:
                data = s.recv(packer.size)
                # ha 0 byte akkor kilepett a kliens
                if not data:
                    socketek.remove(s)
                    s.close()
                    print("Client left.")
                else:
                    print("Recieved:", data)
                    unpacked_data = packer.unpack(data)
                    
                    print("Unpacked:", unpacked_data)
                    number = unpacked_data[0]

                    print(json_dict[str(number)])
                    
                    key = str(number)
                    if not key in json_dict.keys():
                        result = "{0}|sikertelen".format(number)
                        s.sendall(result.encode())
                        print(number, 'hely nem szerepel az adatok közt.')
                    elif json_dict[key] == 'szabad':
                        json_dict[key] = 'foglalt'
                        result = "{0}|sikeres".format(number)
                        s.sendall(result.encode())
                        print(number, 'helyen foglalás történt.')
                    else:
                        result = "{0}|sikertelen".format(number)
                        s.sendall(result.encode())
                        print(number, 'heyen a foglalás sikertelen.')