import sys
import json
import struct
import random, time
from socket import socket, AF_INET, SOCK_STREAM, timeout, SOL_SOCKET, SO_REUSEADDR

server_addr = ('localhost', 10000)

packer = struct.Struct('I')

def reserve(num, client):
    packed_data = packer.pack(int(num))
    client.sendall(packed_data)
            
    data = client.recv(16).decode()
    print("result:", data)

    parts = data.split("|")
    if parts[1] == 'sikeres': print('sikeres foglalás')
    else: print('sikertelen foglalás')    

with socket(AF_INET, SOCK_STREAM) as client:
    client.connect(server_addr)

    if len(sys.argv) == 1:
        num = input("number: ")

        for i in range(0,3):
            time.sleep(random.randint(1,5))
            reserve(num, client)

    if len(sys.argv) == 2:
        try:
            requests_dict = {}
            with open(sys.argv[1], 'r') as requests_file: requests_dict = json.load(requests_file)
            if requests_dict:
                nums = requests_dict['nums']
                for num in nums:
                    time.sleep(1)
                    reserve(num, client)
            else:
                print('ERROR:\nError while reading file!'); exit(1)    
        except:
            print('ERROR:\nError while opening file!'); exit(1)
