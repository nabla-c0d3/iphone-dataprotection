import glob
import plistlib
import os
from bplist import BPlistReader

def read_file(filename):
    f = open(filename, "rb")
    data = f.read()
    f.close()
    return data

def write_file(filename,data):
    f = open(filename, "wb")
    f.write(data)
    f.close()

def makedirs(dirs):
    try:
        os.makedirs(dirs)
    except:
        pass

def readPlist(filename):
    f = open(filename,"rb")
    d = f.read(16)
    f.close()
    if d.startswith("bplist"):
        return BPlistReader.plistWithFile(filename)
    else:
        return plistlib.readPlist(filename)

#http://stackoverflow.com/questions/1094841/reusable-library-to-get-human-readable-version-of-file-size
def sizeof_fmt(num):
    for x in ['bytes','KB','MB','GB','TB']:
        if num < 1024.0:
            return "%d%s" % (num, x)
        num /= 1024.0

def xor_strings(a,b):
    r=""
    for i in xrange(len(a)):
        r+= chr(ord(a[i])^ord(b[i]))
    return r

hex = lambda data: " ".join("%02X" % ord(i) for i in data)
ascii = lambda data: "".join(c if 31 < ord(c) < 127 else "." for c in data)

def hexdump(d):
    for i in xrange(0,len(d),16):
        data = d[i:i+16]
        print "%08X | %s | %s" % (i, hex(data), ascii(data))

def search_plist(directory, matchDict):
    for p in map(os.path.normpath, glob.glob(directory + "/*.plist")):
        try:
            d = plistlib.readPlist(p)
            ok = True
            for k,v in matchDict.items():
                if d.get(k) != v:
                    ok = False
                    break
            if ok:
                print "Using plist file %s" % p
                return d
        except:
            continue
