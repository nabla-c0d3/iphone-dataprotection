#!/usr/bin/python

import plistlib
import zipfile
import struct
import sys
from Crypto.Cipher import AES
from util.lzss import decompress_lzss

devices = {"n88ap": "iPhone2,1",
           "n90ap": "iPhone3,1",
           "n92ap": "iPhone3,3",
           "n18ap": "iPod3,1",
           "n81ap": "iPod4,1",
           "k48ap": "iPad1,1"
           }

h=lambda x:x.replace(" ","").decode("hex")
#https://github.com/comex/datautils0/blob/master/make_kernel_patchfile.c
patchs_ios5 = {
    "CSED" : (h("df f8 88 33 1d ee 90 0f a2 6a 1b 68"), h("df f8 88 33 1d ee 90 0f a2 6a 01 23")),
    "AMFI" : (h("D0 47 01 21 40 B1 13 35"), h("00 20 01 21 40 B1 13 35")),
    "_PE_i_can_has_debugger" : (h("38 B1 05 49 09 68 00 29"), h("01 20 70 47 09 68 00 29")),
    "IOAESAccelerator enable UID" : (h("67 D0 40 F6"), h("00 20 40 F6")),
    #not stritcly required, usefull for testing
    "getxattr system": ("com.apple.system.\x00", "com.apple.aaaaaa.\x00"),
}

#grab keys from redsn0w Keys.plist
class IPSWkeys(object):
    def __init__(self, manifest):
        self.keys = {}
        buildi = manifest["BuildIdentities"][0]
        dc = buildi["Info"]["DeviceClass"]
        build = "%s_%s_%s" % (devices.get(dc,dc), manifest["ProductVersion"], manifest["ProductBuildVersion"])
        try:
            rs = plistlib.readPlist("Keys.plist")
        except:
            raise Exception("Get Keys.plist from redsn0w and place it in the current directory")
        for k in rs["Keys"]:
            if k["Build"] == build:
                self.keys = k
                break

    def getKeyIV(self, filename):
        if not self.keys.has_key(filename):
            return None, None
        k = self.keys[filename]
        return k["Key"], k["IV"]
    
def decryptImg3(blob, key, iv):
    assert blob[:4] == "3gmI", "Img3 magic tag"
    data = ""
    for i in xrange(20, len(blob)):
        tag = blob[i:i+4]
        size, real_size = struct.unpack("<LL", blob[i+4:i+12])
        if tag[::-1] == "DATA":
            assert size >= real_size, "Img3 length check"
            data = blob[i+12:i+size]
            break
        i += size
    return AES.new(key, AES.MODE_CBC, iv).decrypt(data)[:real_size]


def main(ipswname):
    ipsw = zipfile.ZipFile(ipswname)
    manifest = plistlib.readPlistFromString(ipsw.read("BuildManifest.plist"))
    kernelname = manifest["BuildIdentities"][0]["Manifest"]["KernelCache"]["Info"]["Path"]
    kernel = ipsw.read(kernelname)
    keys = IPSWkeys(manifest)
    
    key,iv = keys.getKeyIV(kernelname)
    
    if key == None:
        print "No keys found for kernel"
        return
    
    print "Decrypting %s" % kernelname
    kernel = decryptImg3(kernel, key.decode("hex"), iv.decode("hex"))
    assert kernel.startswith("complzss"), "Decrypted kernelcache does not start with \"complzss\" => bad key/iv ?"
    
    print "Unpacking ..."
    kernel = decompress_lzss(kernel)
    assert kernel.startswith("\xCE\xFA\xED\xFE"), "Decompressed kernelcache does not start with 0xFEEDFACE"
    
    for p in patchs_ios5:
        print "Doing %s patch" % p
        s, r = patchs_ios5[p]
        c = kernel.count(s)
        if c != 1:
            print "=> FAIL, count=%d, do not boot that kernel it wont work" % c
        else:
            kernel = kernel.replace(s,r)
    
    outkernel = "%s.patched" % kernelname
    open(outkernel, "wb").write(kernel)
    print "Patched kernel written to %s" % outkernel
    
    ramdiskname = manifest["BuildIdentities"][0]["Manifest"]["RestoreRamDisk"]["Info"]["Path"]
    key,iv = keys.getKeyIV("Ramdisk")
    
    build_cmd = "./build_ramdisk.sh %s %s %s %s" % (ipswname, ramdiskname, key, iv)
    rs_cmd = "redsn0w -i %s -r myramdisk.dmg -k %s" % (ipswname, outkernel)
    rdisk_script="""#!/bin/sh

for VER in 4.2 4.3 5.0
do
    if [ -f "/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS$VER.sdk/System/Library/Frameworks/IOKit.framework/IOKit" ];
    then
        SDKVER=$VER
        echo "Found iOS SDK $SDKVER"
        break
    fi
done
if [ "$SDKVER" == "" ]; then
    echo "iOS SDK not found"
    exit
fi
SDKVER=$SDKVER make -C ramdisk_tools

%s

echo "You can boot the ramdisk using the following command (fix paths)"
echo "%s"
""" % (build_cmd, rs_cmd)
    
    devclass = manifest["BuildIdentities"][0]["Info"]["DeviceClass"]
    scriptname="make_ramdisk_%s.sh" % devclass
    f=open(scriptname, "wb")
    f.write(rdisk_script)
    f.close()
    
    print "Created script %s, you can use it to (re)build the ramdisk"% scriptname
    

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: %s IPSW" % __file__
        sys.exit(-1)
    main(sys.argv[1])
