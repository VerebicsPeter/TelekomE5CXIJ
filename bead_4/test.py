import hashlib

with open('adat.txt', 'rb') as f:
    file_contents = f.read()

    print(file_contents)

    hash = hashlib.md5(file_contents)
    hexd = hash.hexdigest()
    size = hash.digest_size

    print(hexd, 'length:', size)


