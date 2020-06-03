from Crypto import Random
from Crypto.Cipher import AES
from hashlib import md5
import base64

BLOCK_SIZE=16

def bytes_to_key(data, salt, output=48):
    assert len(salt) == 8, len(salt)
    data += salt
    key = md5(data).digest()
    final_key = key
    while len(final_key) < output:
        key = md5(key+data).digest()
        final_key += key
    return final_key[:output]

def unpad(data):
    return data[:-(data[-1] if type(data[-1]) == int else ord(data[-1]))]

def decrypt(message, passphrase):
    encrypted = base64.b64decode(message)
    assert encrypted[0:8] == b"Salted__"
    salt = encrypted[8:16]
    key_iv = bytes_to_key(passphrase, salt, 32+16)
    key = key_iv[:32]
    iv = key_iv[32:]
    aes = AES.new(key, AES.MODE_CBC, iv)
    return unpad(aes.decrypt(encrypted[16:]))

def pad(data):
    length = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
    return data + (chr(length)*length).encode()

def encrypt(message, passphrase):
    salt = Random.new().read(8)
    key_iv = bytes_to_key(passphrase, salt, 32+16)
    key = key_iv[:32]
    iv = key_iv[32:]
    aes = AES.new(key, AES.MODE_CBC, iv)
    return base64.b64encode(b"Salted__" + salt + aes.encrypt(pad(message)))


ctb64 = 'U2FsdGVkX19c1iDO5WaNSKLj6vYJP/4Af2ZPS4QM4eE='
password = 'E11000'.encode()

myval = 'test@test.com'

password = "some password".encode()
ct_b64 = "U2FsdGVkX1+ATH716DgsfPGjzmvhr+7+pzYfUzR+25u0D7Z5Lw04IJ+LmvPXJMpz"

pt = decrypt(ct_b64, password)
print("pt", pt)

print("pt", decrypt(encrypt(pt, password), password))