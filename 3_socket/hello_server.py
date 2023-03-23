import socket
#import sys

TCP_IP = 'localhost'	#sys.argv[1]
TCP_PORT = 10000		#int(sys.argv[2])
BUFFER_SIZE = 1024
reply = b'Hello kliens'

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((TCP_IP, TCP_PORT))
sock.listen(1)

conn, addr = sock.accept()
print('Valaki csatlakozott:', addr)
while True:
    data = conn.recv(BUFFER_SIZE)
    if not data: break
    print("Beérkező üzenet:", data.decode())
    conn.send(reply)
conn.close()
sock.close()