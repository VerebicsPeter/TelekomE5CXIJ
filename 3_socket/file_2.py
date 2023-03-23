import struct
packer = struct.Struct('i3si')
with open('dates.bin', 'wb') as f: # wb - write binary
    for i in range(5):
        values = (2020+i, b'jan', 10+i)
        packed_data = packer.pack(*values)
        f.write(packed_data)

with open('dates.bin', 'rb') as f: # rb - read as binary
    f.seek(packer.size*4)
    data = f.read(packer.size)
    print(packer.unpack(data))

### output: (2024, b'jan’, 14)