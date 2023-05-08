import sys
import struct, hashlib, time
from socket import socket, AF_INET, SOCK_STREAM, timeout, SOL_SOCKET, SO_REUSEADDR
from select import select

if len(sys.argv) != 7:
    print('This program takes 6 arguments!\n(<srv_ip> <srv_port> <chsum_srv_ip> <chsum_srv_port> <file id> <file path>)');exit(1)

server_addr = (sys.argv[1], int(sys.argv[2]))
chsums_addr = (sys.argv[3], int(sys.argv[4]))

file_id = sys.argv[5]
file = sys.argv[6]

with socket(AF_INET,SOCK_STREAM) as server:
    server.bind(server_addr)
    server.listen(1)
    
    client, client_addr = server.accept()
    
    data = client.recv(1024)

    with open(file, 'wb') as f: f.write(data)
        #client.close()
    
    #get the checksum of the data (file content) received
    hash = hashlib.md5(data)
    size = hash.digest_size; hexd = hash.hexdigest()

    request_message = "KI|{0}".format(file_id)

    time.sleep(1) # helyesség miatt

    with socket(AF_INET, SOCK_STREAM) as chsums_server:
        chsums_server.connect(chsums_addr)

    # send the request message to the checksum server
        chsums_server.sendall(request_message.encode())

    # receive the response from the checksum server
        response = chsums_server.recv(32).decode()

        print('Received:', response)

        parts = response.split('|')
        
        if hexd == parts[1]:
            print('CSUM OK')
        else:
            print('CSUM CORRUPTED')