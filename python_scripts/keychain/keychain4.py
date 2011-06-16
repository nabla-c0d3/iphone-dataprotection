from crypto.aes import AESdecryptCBC
import struct

"""
    iOS 4 keychain-2.db data column format

    magic       0x00000000
    key class   0x00000008
                kSecAttrAccessibleWhenUnlocked                      6
                kSecAttrAccessibleAfterFirstUnlock                  7
                kSecAttrAccessibleAlways                            8
                kSecAttrAccessibleWhenUnlockedThisDeviceOnly        9
                kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly    10
                kSecAttrAccessibleAlwaysThisDeviceOnly              11
    wrapped AES256 key 0x28 bytes  (passed to kAppleKeyStoreKeyUnwrap)
    encrypted data (AES 256 CBC zero IV)
"""
from keychain import Keychain

KSECATTRACCESSIBLE = {
    6: "kSecAttrAccessibleWhenUnlocked",
    7: "kSecAttrAccessibleAfterFirstUnlock",
    8: "kSecAttrAccessibleAlways",
    9: "kSecAttrAccessibleWhenUnlockedThisDeviceOnly",
    10: "kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly",
    11: "kSecAttrAccessibleAlwaysThisDeviceOnly"
}

class Keychain4(Keychain):
    def __init__(self, filename, keybag):
        if not keybag.unlocked:
            raise Exception("Keychain4 object created with locked keybag")
        Keychain.__init__(self, filename)
        self.keybag = keybag

    def decrypt_data(self, blob):
        if blob == None:
            return ""
        
        if len(blob) < 48:
            print "keychain blob length must be >= 48"
            return

        magic, clas = struct.unpack("<LL",blob[0:8])

        if magic != 0:
            print "keychain blob first dword not 0"
            return

        wrappedkey = blob[8:8+40]
        encrypted_data = blob[48:]
        unwrappedkey = self.keybag.unwrapKeyForClass(clas, wrappedkey)
        if not unwrappedkey:
            print "keychain decrypt fail for item with class=%d (%s)" % (clas, KSECATTRACCESSIBLE.get(clas))
            return

        return AESdecryptCBC(encrypted_data, unwrappedkey, padding=True)