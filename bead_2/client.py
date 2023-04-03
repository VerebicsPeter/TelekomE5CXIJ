import sys
import struct

if len(sys.argv) != 5:
    print("This program takes 4 arguments!")
    exit(1)

def unpackFormat(i, fstring) :
    with open(sys.argv[i],'rb') as file:
        packed = file.read()
        packer = struct.Struct(fstring)
        return packer.unpack(packed)

def packFormat(data, fstring) :
    packer = struct.Struct(fstring)
    return packer.pack(*data)

res1 = unpackFormat(1, 'c 9s i')
res2 = unpackFormat(2, 'i f ?')
res3 = unpackFormat(3, '? 9s c')
res4 = unpackFormat(4, 'i c f')

print(res1);print(res2);print(res3);print(res4)

tpl1 = (b"elso", 53, True)     # str is 13
tpl2 = (56.5, False, 'X') 
tpl3 = (44, b"masodik", 63.9)  # str is 11
tpl4 = ('Z', 75, b"harmadik")  # str is 14

print(packFormat(tpl1, '13s i ?'))
print(packFormat(tpl2, 'f ? c'))
print(packFormat(tpl3, 'i 11s f'))
print(packFormat(tpl3, 'c i 14s'))
