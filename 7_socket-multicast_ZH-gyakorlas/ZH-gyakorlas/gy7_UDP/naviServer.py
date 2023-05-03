from socket import socket, AF_INET, SOCK_DGRAM, timeout
import struct

proxy_addr = ('localhost',10002)
server_addr = ('localhost',10001)
packer = struct.Struct("I I I I")

with socket(AF_INET, SOCK_DGRAM) as proxy, socket(AF_INET, SOCK_DGRAM) as server:

    proxy.bind(proxy_addr)
    proxy.settimeout(1.0)

    server.connect(proxy_addr)

    while True:
        try:
            data, client = proxy.recvfrom(128)

            decoded_data = data.decode()

            print("recieved:", decoded_data, "from:", client)
            strings = decoded_data.split(';')
            to_send = packer.pack(
						int(strings[0]),
						int(strings[1]),
						int(strings[2]),
						int(strings[3]))
            
            server.sendto(to_send, server_addr)
            response = proxy.recvfrom(128)
            proxy.sendto(response[0], client)
        except timeout:
            pass