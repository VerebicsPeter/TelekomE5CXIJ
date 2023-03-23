import socket

for i in range(1,101):
    try:
        print(i,":",socket.getservbyport(i))
    except OSError:
        print(i,": nincs tartozik hozzá semmi")