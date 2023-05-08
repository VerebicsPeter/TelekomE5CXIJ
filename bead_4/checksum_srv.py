import sys
import struct, hashlib, time
from socket import socket, AF_INET, SOCK_STREAM, timeout, SOL_SOCKET, SO_REUSEADDR
from select import select

checksum_data = []

def insert_checksum_data(fileID, exp, checksum_length, checksum_bytes):
    elem = {"id":fileID,"exp":time.time()+float(exp),"csum_len":checksum_length,"csum_bytes":checksum_bytes}
    checksum_data.append(elem)

def remove_expired_data():
    now = time.time()
    non_expired = [elem for elem in checksum_data if elem['exp'] > now]
    checksum_data.clear()
    checksum_data.extend(non_expired)

def remove_checksum_data(fileID):
    remove_expired_data()
    result = {}
    for elem in checksum_data:
        if elem['id'] == fileID: result = elem
    checksum_data.remove(result)
    return result

if len(sys.argv) != 3:
    print('This program takes 2 arguments!\n(<ip> <port>)');exit(1)

server_addr = (sys.argv[1], int(sys.argv[2]))

with socket(AF_INET, SOCK_STREAM) as server:
    server.bind(server_addr)
    server.listen(1)
    server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    
    socketek = [ server ]
    
    while True:
        r,w,e = select(socketek,[],[],1)
        
        if not (r or w or e): continue
        
        for s in r:
            if s is server:
                # kliens csatlakozik
                client, client_addr = s.accept()
                socketek.append(client)
                print("Client connected.", client_addr)
            else:
                data = s.recv(32)
                # ha 0 byte akkor kilepett a kliens
                if not data:
                    socketek.remove(s)
                    s.close()
                    print("Client left.")
                else:
                    print("Received:", data)
                    decoded_data = data.decode()

                    parts = decoded_data.split('|')
                    # sent from a client
                    if parts[0] == "BE":
                        insert_checksum_data(parts[1], parts[2], parts[3], parts[4])
                        s.sendall(b"OK")
                    # sent from the server
                    if parts[0] == "KI":
                        elem = remove_checksum_data(parts[1])
                        if elem:
                            response = "{0}|{1}".format(elem['csum_len'],elem['csum_bytes'])
                            s.sendall(response.encode())
                        else:
                            s.sendall(b"0|")