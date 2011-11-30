#!/usr/bin/python

import plistlib
import zipfile
import struct
import sys
from optparse import OptionParser
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
    #not stritcly required, useful for testing
    "getxattr system": ("com.apple.system.\x00", "com.apple.aaaaaa.\x00"),
}

patchs_ios4 = {
    "NAND_epoch" : ("\x90\x47\x83\x45", "\x90\x47\x00\x20"),
    "CSED" : ("\x00\x00\x00\x00\x01\x00\x00\x00\x80\x00\x00\x00\x00\x00\x00\x00", "\x01\x00\x00\x00\x01\x00\x00\x00\x80\x00\x00\x00\x00\x00\x00\x00"),
    "AMFI" : ("\x01\xD1\x01\x30\x04\xE0\x02\xDB", "\x00\x20\x01\x30\x04\xE0\x02\xDB"),
    "_PE_i_can_has_debugger" : (h("48 B1 06 4A 13 68 13 B9"), h("01 20 70 47 13 68 13 B9")),
    "IOAESAccelerator enable UID" : ("\x56\xD0\x40\xF6", "\x00\x00\x40\xF6"),
    "getxattr system": ("com.apple.system.\x00", "com.apple.aaaaaa.\x00"),
}

patchs_ios4_fixnand = {
    "Please reboot => jump to prepare signature": (h("B0 47 DF F8 E8 04 F3 E1"), h("B0 47 DF F8 E8 04 1D E0")),
    "prepare signature => jump to write signature": (h("10 43 18 60 DF F8 AC 04"), h("10 43 18 60 05 E1 00 20")),
    "check write ok => infinite loop" : (h("A3 48 B0 47 01 24"), h("A3 48 B0 47 FE E7"))
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
        return k.get("Key",""), k.get("IV","")
    
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


def main(ipswname, options):
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
    
    patchs = patchs_ios5
    if manifest["ProductVersion"].startswith("4."):
        print "Using iOS 4 kernel patches"
        patchs = patchs_ios4
    
    if options.fixnand:
        if patchs != patchs_ios4:
            print "FAIL : use --fixnand with iOS 4.x IPSW"
            return
        patchs.update(patchs_ios4_fixnand)
        kernelname = "fix_nand_" + kernelname
        print "WARNING : only use this kernel to fix NAND epoch brick"
    
    for p in patchs:
        print "Doing %s patch" % p
        s, r = patchs[p]
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
    parser = OptionParser(usage="%prog [options] IPSW")
    parser.add_option("-f", "--fixnand",
                      action="store_true", dest="fixnand", default=False,
                      help="Apply NAND epoch fix kernel patches")
    
    (options, args) = parser.parse_args()
    if len(args) < 1:
        parser.print_help()
    else:
        main(args[0], options)
