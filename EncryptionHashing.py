import hashlib
import json
from random import randint, randrange  
from math import sqrt
from Crypto.PublicKey import ECC
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from base64 import b64encode
from FileManage import *
import pbkdf2

def gen_key_export(username, password):
    key = ECC.generate(curve = 'P-256')
    filename = username+"key"
    f = open(ECC_key_dir(filename), 'wb')
    f.write(key.export_key(format = 'DER', passphrase = password, use_pkcs8 = True, protection = 'PBKDF2WithHMAC-SHA1AndAES128-CBC'))
    f.close()
#gen_key_export('arjun', 'arjun2000')

def get_key(username, password):
    filename = username+'key'
    try:
        f  = open(ECC_key_dir(filename), 'rb')
        key = ECC.import_key(f.read(), password)
    except:
        gen_key_export(username, password)
        return get_key(username, password)
    else:
        return key
#print(get_key('arjun', 'arjun2000'))

def generate_secret_key(user_key, sender_public_key): #receives the sender key and generates the secret pair key
    '''
    sender_public_key is of type ECCPoint
    user_key is also of type key
    '''
    #Assigining user_key to an ecc point
    Secret_Key = user_key.d*sender_public_key
    salt = b'\x05;iBi\x17Q\xe0'
    Secret_Pair_Key = pbkdf2.PBKDF2(str(Secret_Key.x), salt).read(32) # Generating a 256-bit key
    return Secret_Pair_Key

def generate_AES_key():
    AES_key = get_random_bytes(32)
    return AES_key

def encryption(key, plaintext):
    '''username should be appended with a unique code'''
    try:
        data = bytes(plaintext, 'utf-8')
        cipher = AES.new(key, AES.MODE_GCM)
        ciphertext, tag = cipher.encrypt_and_digest(data)
        encrypted_data = {'ciphertext': ciphertext, 'tag': tag, 'nonce': cipher.nonce}
    except:
        return False
    else:
        return encrypted_data

'''    
key = generate_AES_key()
e_d = encryption(key, 'arjun wrote this')
print(e_d)
'''

def decryption(key, encrypted_data):
    try:
        header: encrypted_data['header']
        data = encrypted_data['ciphertext']
        cipher = AES.new(key, AES.MODE_GCM, encrypted_data['nonce'])
        plaintext = cipher.decrypt_and_verify(data, encrypted_data['tag'])
    except:
        return False
    else:
        return plaintext.decode('utf-8')

'''print(decryption(key, e_d))'''

def hash_str(credential): #for hashing passwords
    hashed_string=hashlib.sha256(str.encode(credential))
    hashed_string_hex = hashed_string.digest()
    return hashed_string_hex