#import sys
import socket
import struct

TCP_IP = 'localhost'	#sys.argv[1]
TCP_PORT = 10000		#int(sys.argv[2])
BUFFER_SIZE = 1024

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((TCP_IP, TCP_PORT))
sock.listen(1)

# csunya szar megoldas VVV
def calc_result(unpacked_data):
    x, y = unpacked_data[0], unpacked_data[2]
    if unpacked_data[1] == b'+':
        return x + y
    if unpacked_data[1] == b'-':
        return x - y
    if unpacked_data[1] == b'*':
        return x * y
    if unpacked_data[1] == b'/':
        return x / y
    if unpacked_data[1] == b'%':
        return x % y
    if unpacked_data[1] == b'^':
        return x ** y
    return 'operator not recognized'

conn, addr = sock.accept()
print('Valaki csatlakozott:', addr)
while True:
    data = conn.recv(BUFFER_SIZE)
    if not data: break
    packer = struct.Struct('f 1s f')
    size = packer.size
    unpacked_data = packer.unpack(data)
    print("Beérkező üzenet:", unpacked_data)
    result = calc_result(unpacked_data)
    conn.send(str(result).encode())

conn.close()
sock.close()

# szebb megoldas: calcServer