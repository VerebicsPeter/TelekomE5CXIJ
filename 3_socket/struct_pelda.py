import struct

values = (1, 'ab', 2.7)
packer = struct.Struct('i 2s f')
packed_data = packer.pack(*values)
# HIBA: struct.error: argument for 's' must be a bytes object
# JÓ megoldás:
#values = (1, b'ab', 2.7) # vagy values = (1, 'ab'.encode(), 2.7)

size1 = struct.calcsize('i 2s f')
size2 = packer.size
unpacked_data = packer.unpack(packed_data)

print("""
	Struktura
	
	Kod:
	import struct

	values = (1, 'ab'.encode(), 2.7)
	print(values)				#""", values, """
	
	packer = struct.Struct('i 2s f')
	print(packer)				#""" ,packer,"""
	
	packed_data = packer.pack(*values)
	print(packed_data)			#""" ,packed_data,"""

	struct.calcsize('i 2s f')		#""" ,size1,"""
	packer.size				#""" ,size2,"""
	
	unpacked_data = packer.unpack(packed_data)
	print(packed_data)			#""" ,unpacked_data,"""
	""",'\n')