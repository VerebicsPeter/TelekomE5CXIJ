import binascii
import zlib

test_string = "Fekete retek rettenetes".encode('utf-8')

b = hex(binascii.crc32(bytearray(test_string)))
z = hex(zlib.crc32(test_string))

print(b)
print(z)
