from keychain import Keychain
from crypto.aes import AESdecryptCBC
import hashlib

class Keychain3(Keychain):
    def __init__(self, filename, key835=None):
        Keychain.__init__(self, filename)
        self.key835 = key835
        
    def decrypt_data(self, data):
        data = str(data)
        
        if not self.key835:
            print "Key 835 not availaible"
            return ""
        
        data = AESdecryptCBC(data[16:], self.key835, data[:16], padding=True)
        
        #data_column = iv + AES128_K835(iv, data + sha1(data))
        if hashlib.sha1(data[:-20]).digest() != data[-20:]:
            print "data field hash mismatch : bad key ?"
            return "ERROR decrypting data : bad key ?"

        return data[:-20]