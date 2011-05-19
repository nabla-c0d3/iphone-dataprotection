import struct
from Crypto.Cipher import AES

"""
    http://www.ietf.org/rfc/rfc3394.txt
    quick'n'dirty AES wrap implementation
    used by iOS 4 KeyStore kernel extension for wrapping/unwrapping encryption keys
"""
def unpack64bit(s):
    return struct.unpack(">Q",s)[0]
def pack64bit(s):
    return struct.pack(">Q",s)

def AESUnwrap(kek, wrapped):
    C = []
    for i in xrange(len(wrapped)/8):
        C.append(unpack64bit(wrapped[i*8:i*8+8]))
    n = len(C) - 1
    R = [0] * (n+1)
    A = C[0]
    
    for i in xrange(1,n+1):
        R[i] = C[i]
    
    for j in reversed(xrange(0,6)):
        for i in reversed(xrange(1,n+1)):
            todec = pack64bit(A ^ (n*j+i))
            todec += pack64bit(R[i])
            B = AES.new(kek).decrypt(todec)
            A = unpack64bit(B[:8])
            R[i] = unpack64bit(B[8:])
    
    #assert A == 0xa6a6a6a6a6a6a6a6, "AESUnwrap: integrity check FAIL, wrong kek ?"
    if A != 0xa6a6a6a6a6a6a6a6:
        #print "AESUnwrap: integrity check FAIL, wrong kek ?"
        return None    
    res = "".join(map(pack64bit, R[1:]))
    return res