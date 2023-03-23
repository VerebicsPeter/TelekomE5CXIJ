import struct

string = 'hello'
string = string.encode() # b’hello’
print(string)

d = struct.pack('8s',string) #b’hello\x00\x00\x00’
print(d)
d = d.decode().strip('\x00') #’hello’
print(d)