import hashlib
from random import randint, randrange  
from math import sqrt
from Crypto.PublicKey import ECC
from FileManage import *
import pbkdf2

def gen_key_export(username, password):
    key = ECC.generate(curve = 'P-256')
    filename = username+"key"
    f = open(Return_App_Path(filename), 'wb')
    f.write(key.export_key(format = 'DER', passphrase = password, use_pkcs8 = True, protection = 'PBKDF2WithHMAC-SHA1AndAES128-CBC'))
    f.close()
#gen_key_export('arjun', 'arjun2000')

def get_key(username, password):
    filename = username+'key'
    try:
        f  = open(Return_App_Path(filename), 'rb')
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
    key_b_32_bytes = pbkdf2.PBKDF2(str(Secret_Key.x), salt).read(32) # Generating a 256-bit key

def hash_str(credential): #for hashing passwords
    hashed_string=hashlib.sha256(str.encode(credential))
    hashed_string_hex = hashed_string.digest()
    return hashed_string_hex
