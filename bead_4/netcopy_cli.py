import sys
import struct, hashlib
from socket import socket, AF_INET, SOCK_STREAM

if len(sys.argv) != 7:
    print('This program takes 6 arguments!\n(<srv_ip> <srv_port> <chsum_srv_ip> <chsum_srv_port> <file id> <file path>)');exit(1)

server_addr = (sys.argv[1], int(sys.argv[2]))
chsums_addr = (sys.argv[3], int(sys.argv[4]))

file_id = sys.argv[5]
file = sys.argv[6]

with socket(AF_INET,SOCK_STREAM) as client:
    with open(file, "rb") as f:
        client.connect(server_addr)
        file_content = f.read()
        client.sendall(file_content)
        print("Sent file.")
        
        hash = hashlib.md5(file_content)
        size = hash.digest_size; hexd = hash.hexdigest()
        print('hash:', hexd, 'length:', size)

    with socket(AF_INET, SOCK_STREAM) as chsum_client:
        chsum_client.connect(chsums_addr)
        
        message = "BE|{0}|60|{1}|{2}".format(file_id,size,hexd)
        chsum_client.sendall(message.encode())
        data = chsum_client.recv(10).decode()

        print('Received from checksum server:', data)
