import hashlib
import binascii

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

class AESCipher:
    def __init__(self, req_key, req_salt, res_key, res_salt):
        listdata = [0, 1, 2, 3, 4, 5, 6, 7,
                    8, 9, 10, 11, 12, 13, 14, 15]
        self.byteArrayObject = bytearray(listdata)

        self.requestEncypritonKey = req_key.encode()
        self.requestSaltkey = req_salt.encode()
        self.responseDecypritonKey = res_key.encode()
        self.responseSaltkey = res_salt.encode()
        
    def encrypt( self, message ):
        pbkdf2_hmac_key = hashlib.pbkdf2_hmac('sha512', self.requestEncypritonKey, self.requestSaltkey, 65536, dklen=32)
        cipher = AES.new(pbkdf2_hmac_key, AES.MODE_CBC, self.byteArrayObject)
        cipher_enc = cipher.encrypt(pad(message, 16))
        return cipher_enc.hex().upper()
    
    def decrypt( self, message ):
        binary_string = binascii.unhexlify(message.strip())
        pbkdf2_hmac_key = hashlib.pbkdf2_hmac('sha512', self.responseDecypritonKey, self.responseSaltkey, 65536, dklen=32)
        cipher = AES.new(pbkdf2_hmac_key, AES.MODE_CBC, self.byteArrayObject)
        cipher_dec = cipher.decrypt(binary_string)
        return cipher_dec.decode('utf-8')
