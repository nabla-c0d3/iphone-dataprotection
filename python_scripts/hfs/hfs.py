import os
import sys
import struct
import zlib
from btree import AttributesTree, CatalogTree, ExtentsOverflowTree
from structs import *
from util import write_file

class HFSFile(object):
    def __init__(self, volume, hfsplusfork, fileID, deleted=False):
        self.volume = volume
        self.blockSize = volume.blockSize
        self.fileID = fileID
        self.totalBlocks = hfsplusfork.totalBlocks
        self.logicalSize = hfsplusfork.logicalSize
        self.extents = []
        self.deleted = deleted
        b = 0
        for extent in hfsplusfork.HFSPlusExtentDescriptor:
            self.extents.append(extent)
            b += extent.blockCount
        while b != hfsplusfork.totalBlocks:
            #print "extents overflow ", b
            k,v = volume.getExtentsOverflowForFile(fileID, b)
            if not v:
                print "extents overflow missing, startblock=%d" % b
                break
            for extent in v:
                self.extents.append(extent)
                b += extent.blockCount

    def readAll(self, outputfile, truncate=True):
        f = open(outputfile, "wb")
        for i in xrange(self.totalBlocks):
            f.write(self.readBlock(i))
        if truncate:
            f.truncate(self.logicalSize)
        f.close()

    def readAllBuffer(self, truncate=True):
        r = ""
        for i in xrange(self.totalBlocks):
            r += self.readBlock(i)
        if truncate:
            r = r[:self.logicalSize]
        return r

    def processBlock(self, block, lba):
        return block

    def readBlock(self, n):
        bs = self.volume.blockSize
        if n*bs > self.logicalSize:
            return "BLOCK OUT OF BOUNDS" + "\xFF" * (bs - len("BLOCK OUT OF BOUNDS"))
        bc = 0
        for extent in self.extents:
            bc += extent.blockCount
            if n < bc:
                lba = extent.startBlock+(n-(bc-extent.blockCount))
                if not self.deleted and self.fileID != kHFSAllocationFileID and  not self.volume.isBlockInUse(lba):
                    print "FAIL, block %x not marked as used" % n
                return self.processBlock(self.volume.read(lba*bs, bs), lba)
        return ""

class HFSCompressedResourceFork(HFSFile):
    def __init__(self, volume, hfsplusfork, fileID):
        super(HFSCompressedResourceFork,self).__init__(volume, hfsplusfork, fileID)
        block0 = self.readBlock(0)
        self.header = HFSPlusCmpfRsrcHead.parse(block0)
        print self.header
        self.blocks = HFSPlusCmpfRsrcBlockHead.parse(block0[self.header.headerSize:])
        print "HFSCompressedResourceFork numBlocks:", self.blocks.numBlocks

    #HAX, readblock not implemented
    def readAllBuffer(self):
        buff = super(HFSCompressedResourceFork, self).readAllBuffer()
        r = ""
        base = self.header.headerSize + 4
        for b in self.blocks.HFSPlusCmpfRsrcBlock:
            r += zlib.decompress(buff[base+b.offset:base+b.offset+b.size])
        return r

class HFSVolume(object):
    def __init__(self, filename, write=False, offset=0):
        flag = os.O_RDONLY if not write else os.O_RDWR
        if sys.platform == 'win32':
            flag = flag | os.O_BINARY
        self.fd = os.open(filename, flag)
        self.offset = offset
        self.writeFlag = write

        try:
            data = self.read(0, 0x1000)
            self.header = HFSPlusVolumeHeader.parse(data[0x400:0x800])
            assert self.header.signature == 0x4858 or self.header.signature == 0x482B
        except:
            raise Exception("Not an HFS+ image")

        self.blockSize = self.header.blockSize

        if os.path.getsize(filename) < self.header.totalBlocks * self.blockSize:
            print "WARNING: image appears to be truncated"

        self.allocationFile = HFSFile(self, self.header.allocationFile, kHFSAllocationFileID)
        self.allocationBitmap = self.allocationFile.readAllBuffer()
        self.extentsFile = HFSFile(self, self.header.extentsFile, kHFSExtentsFileID)
        self.extentsTree = ExtentsOverflowTree(self.extentsFile)
        self.catalogFile = HFSFile(self, self.header.catalogFile, kHFSCatalogFileID)
        self.xattrFile = HFSFile(self, self.header.attributesFile, kHFSAttributesFileID)
        self.catalogTree = CatalogTree(self.catalogFile)
        self.xattrTree = AttributesTree(self.xattrFile)

        self.hasJournal = self.header.attributes & (1 << kHFSVolumeJournaledBit)

    def read(self, offset, size):
        os.lseek(self.fd, self.offset + offset, os.SEEK_SET)
        return os.read(self.fd, size)

    def write(self, offset, data):
        if self.writeFlag: #fail silently for testing 
            os.lseek(self.fd, self.offset + offset, os.SEEK_SET)
            return os.write(self.fd, data)

    def writeBlock(self, lba, block):
        return self.write(lba*self.blockSize, block)

    def volumeID(self):
        return struct.pack(">LL", self.header.finderInfo[6], self.header.finderInfo[7])

    def isBlockInUse(self, block):
        thisByte = ord(self.allocationBitmap[block / 8])
        return (thisByte & (1 << (7 - (block % 8)))) != 0

    def unallocatedBlocks(self):
        for i in xrange(self.header.totalBlocks):
            if not self.isBlockInUse(i):
                yield i, self.read(i*self.blockSize, self.blockSize)

    def getExtentsOverflowForFile(self, fileID, startBlock, forkType=kForkTypeData):
        return self.extentsTree.searchExtents(fileID, forkType, startBlock)

    def getXattr(self, fileID, name):
        return self.xattrTree.searchXattr(fileID, name)

    def getFileByPath(self, path):
        return self.catalogTree.getRecordFromPath(path)

    def listFolderContents(self, path):
        k,v = self.catalogTree.getRecordFromPath(path)
        if not k or v.recordType != kHFSPlusFolderRecord:
            return
        for k,v in self.catalogTree.getFolderContents(v.data.folderID):
            if v.recordType == kHFSPlusFolderRecord:
                print v.data.folderID, getString(k) + "/"
            elif v.recordType == kHFSPlusFileRecord:
                print v.data.fileID, getString(k)

    def listXattrs(self, path):
        k,v = self.catalogTree.getRecordFromPath(path)
        if k and v.recordType == kHFSPlusFileRecord:
            return self.xattrTree.getAllXattrs(v.data.fileID)
        elif k and v.recordType == kHFSPlusFolderThreadRecord:
            return self.xattrTree.getAllXattrs(v.data.folderID)

    def readFile(self, path, returnString=False):
        k,v = self.catalogTree.getRecordFromPath(path)
        if not v:
            print "File %s not found" % path
            return
        assert v.recordType == kHFSPlusFileRecord
        xattr = self.getXattr(v.data.fileID, "com.apple.decmpfs")
        if xattr:
            decmpfs = HFSPlusDecmpfs.parse(xattr)

            if decmpfs.compression_type == 1:
                return xattr[16:]
            elif decmpfs.compression_type == 3:
                if decmpfs.uncompressed_size == len(xattr) - 16:
                    return xattr[16:]
                return zlib.decompress(xattr[16:])
            elif decmpfs.compression_type == 4:
                f = HFSCompressedResourceFork(self, v.data.resourceFork, v.data.fileID)
                return f.readAllBuffer()

        f = HFSFile(self, v.data.dataFork, v.data.fileID)
        if returnString:
            return f.readAllBuffer()
        else:
            f.readAll(os.path.basename(path))

    def readJournal(self):
        jb = self.read(self.header.journalInfoBlock * self.blockSize, self.blockSize)
        jib = JournalInfoBlock.parse(jb)
        return self.read(jib.offset,jib.size)

if __name__ == "__main__":
    v = HFSVolume("myramdisk.dmg",offset=0x40)
    v.listFolderContents("/")
    print v.readFile("/usr/local/share/restore/imeisv_svn.plist")
    print v.listXattrs("/usr/local/share/restore/imeisv_svn.plist")
