import plistlib
import os
import struct
from hfs import HFSVolume, HFSFile
from keystore.keybag import Keybag
from structs import HFSPlusVolumeHeader, kHFSPlusFileRecord, getString
from construct import Struct, ULInt16,ULInt32, String
from Crypto.Cipher import AES
from construct.macros import ULInt64, Padding
from structs import kHFSRootParentID
import hashlib

"""
iOS >= 4 raw images
http://opensource.apple.com/source/xnu/xnu-1699.22.73/bsd/hfs/hfs_cprotect.c
http://opensource.apple.com/source/xnu/xnu-1699.22.73/bsd/sys/cprotect.h
"""

cp_root_xattr = Struct("cp_root_xattr",
    ULInt16("major_version"),
    ULInt16("minor_version"),
    ULInt64("flags"),
    ULInt32("reserved1"),
    ULInt32("reserved2"),
    ULInt32("reserved3"),
    ULInt32("reserved4")
)

cprotect_xattr = Struct("cprotect_xattr",
    ULInt16("xattr_major_version"),
    ULInt16("xattr_minor_version"),
    ULInt32("flags"),
    ULInt32("persistent_class"),
    ULInt32("key_size"),
    String("persistent_key", length=0x28)
)

cprotect4_xattr = Struct("cprotect_xattr",
    ULInt16("xattr_major_version"),
    ULInt16("xattr_minor_version"),
    ULInt32("flags"),
    ULInt32("persistent_class"),
    ULInt32("key_size"),
    Padding(20),
    String("persistent_key", length=lambda ctx: ctx["key_size"])
)

#HAX: flags set in finderInfo[3] to tell if the image was already decrypted
FLAG_DECRYPTING = 0x454d4664  #EMFd big endian
FLAG_DECRYPTED = 0x454d4644  #EMFD big endian

class EMFFile(HFSFile):
    def __init__(self, volume, hfsplusfork, fileID, filekey, deleted=False):
        super(EMFFile,self).__init__(volume, hfsplusfork, fileID, deleted)
        self.filekey = filekey
        self.ivkey = None
        self.decrypt_offset = 0
        if volume.cp_root.major_version == 4:
            self.ivkey = hashlib.sha1(filekey).digest()[:16]

    def processBlock(self, block, lba):
        iv = self.volume.ivForLBA(lba)
        ciphertext = AES.new(self.volume.emfkey, AES.MODE_CBC, iv).encrypt(block)
        if not self.ivkey:
            clear = AES.new(self.filekey, AES.MODE_CBC, iv).decrypt(ciphertext)
        else:
            clear = ""
            for i in xrange(len(block)/0x1000):
                iv = self.volume.ivForLBA(self.decrypt_offset, False)
                iv = AES.new(self.ivkey).encrypt(iv)
                clear += AES.new(self.filekey, AES.MODE_CBC, iv).decrypt(ciphertext[i*0x1000:(i+1)*0x1000])
                self.decrypt_offset += 0x1000
        return clear
    
    def decryptFile(self):
        self.decrypt_offset = 0
        bs = self.volume.blockSize
        for extent in self.extents:
            for i in xrange(extent.blockCount):
                lba = extent.startBlock+i
                data = self.volume.read(lba*bs, bs)
                if len(data) == bs:
                    clear = self.processBlock(data, lba)
                    self.volume.writeBlock(lba, clear)


class EMFVolume(HFSVolume):
    def __init__(self, file, **kwargs):
        super(EMFVolume,self).__init__(file, **kwargs)
        pl = "%s.plist" % self.volumeID().encode("hex")
        dirname = os.path.dirname(file)
        if dirname != "":
            pl = dirname + "/" + pl
        if not os.path.exists(pl):
            raise Exception("Missing keyfile %s" % pl)
        try:
            pldict = plistlib.readPlist(pl)
            self.emfkey = pldict["EMF"].decode("hex")
            self.lbaoffset = pldict["dataVolumeOffset"]
            self.keystore = Keybag.createWithPlist(pldict)
        except:
            raise #Exception("Invalid keyfile")
        
        rootxattr =  self.getXattr(kHFSRootParentID, "com.apple.system.cprotect")
        if rootxattr == None:
            print "Not an EMF image, no root com.apple.system.cprotec xattr"
        else:
            self.cp_root = cp_root_xattr.parse(rootxattr)
            print "cprotect version :", self.cp_root.major_version
            assert self.cp_root.major_version == 2 or self.cp_root.major_version == 4
    
    def ivForLBA(self, lba, add=True):
        iv = ""
        if add:
            lba = lba + self.lbaoffset
        for _ in xrange(4):
            if (lba & 1):
                lba = 0x80000061 ^ (lba >> 1);
            else:
                lba = lba >> 1;
            iv += struct.pack("<L", lba)
        return iv
    
    def getFileKeyForCprotect(self, cp):
        if self.cp_root.major_version == 2:
            cprotect = cprotect_xattr.parse(cp)
        elif self.cp_root.major_version == 4:
            cprotect = cprotect4_xattr.parse(cp)
        return self.keystore.unwrapKeyForClass(cprotect.persistent_class, cprotect.persistent_key)
    
    def readFile(self, path, outFolder="./"):
        k,v = self.catalogTree.getRecordFromPath(path)
        if not v:
            print "File %s not found" % path
            return
        assert v.recordType == kHFSPlusFileRecord
        cprotect = self.getXattr(v.data.fileID, "com.apple.system.cprotect")
        if cprotect == None:
            print "cprotect attr not found, reading normally"
            return super(EMFVolume, self).readFile(path)
        filekey = self.getFileKeyForCprotect(cprotect)
        if not filekey:
            print "Cannot unwrap file key for file %s protection_class=%d" % (path, cprotect.protection_class)
            return
        f = EMFFile(self, v.data.dataFork, v.data.fileID, filekey)
        f.readAll(outFolder + os.path.basename(path))

    def flagVolume(self, flag):
        self.header.finderInfo[3] = flag
        h = HFSPlusVolumeHeader.build(self.header)
        return self.write(0x400, h)
        
    def decryptAllFiles(self):
        if self.header.finderInfo[3] == FLAG_DECRYPTING:
            print "Volume is half-decrypted, aborting (finderInfo[3] == FLAG_DECRYPTING)"
            return
        elif self.header.finderInfo[3] == FLAG_DECRYPTED:
            print "Volume already decrypted (finderInfo[3] == FLAG_DECRYPTED)"
            return
        self.failedToGetKey = []
        self.notEncrypted = []
        self.decryptedCount = 0
        self.flagVolume(FLAG_DECRYPTING)
        self.catalogTree.traverseLeafNodes(callback=self.decryptFile)
        self.flagVolume(FLAG_DECRYPTED)
        print "Decrypted %d files" % self.decryptedCount
        print "Failed to unwrap keys for : ", self.failedToGetKey
        print "Not encrypted files : %d" % len(self.notEncrypted)

    def decryptFile(self, k,v):
        if v.recordType == kHFSPlusFileRecord:
            filename = getString(k)
            cprotect = self.getXattr(v.data.fileID, "com.apple.system.cprotect")
            if not cprotect:
                self.notEncrypted.append(filename)
                return
            fk = self.getFileKeyForCprotect(cprotect)
            if not fk:
                self.failedToGetKey.append(filename)
                return
            print "Decrypting", filename
            f = EMFFile(self, v.data.dataFork, v.data.fileID, fk)
            f.decryptFile()
            self.decryptedCount += 1
