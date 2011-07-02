#!/usr/bin/env python

import os
import sys
from struct import pack, unpack
from Crypto.Cipher import AES
from crypto.aeswrap import AESUnwrap
from util.bplist import BPlistReader
from keystore.keybag import Keybag
from pprint import pprint

MBDB_SIGNATURE = 'mbdb\x05\x00'
MBDX_SIGNATURE = 'mbdx\x02\x00'

MASK_SYMBOLIC_LINK = 0xa000
MASK_REGULAR_FILE = 0x8000
MASK_DIRECTORY = 0x4000

class MBFileRecord(object):
    def __init__(self, mbdb):
        self.domain = self._decode_string(mbdb)
        if self.domain is None:
            warn("Domain name missing from record")

        self.path = self._decode_string(mbdb)
        if self.path is None:
            warn("Relative path missing from record")

        self.target= self._decode_string(mbdb) # for symbolic links

        self.digest = self._decode_string(mbdb)
        self.encryption_key = self._decode_data(mbdb)

        data = mbdb.read(40) # metadata, fixed size

        self.mode, = unpack('>H', data[0:2])
        if not(self.is_regular_file() or self.is_symbolic_link() or self.is_directory()):
            warn("File type mising from record mode")

        if self.is_symbolic_link() and self.target is None:
            warn("Target required for symblolic links")

        self.inode_number = unpack('>Q', data[2:10])
        self.user_id, = unpack('>I', data[10:14])
        self.group_id = unpack('>I', data[14:18])
        self.last_modification_time, = unpack('>i', data[18:22])
        self.last_status_change_time, = unpack('>i', data[22:26])
        self.birth_time, = unpack('>i', data[26:30])
        self.size, = unpack('>q', data[30:38])

        if self.size != 0 and not self.is_regular_file():
            warn("Non-zero size for a record which is not a regular file")

        self.protection_class = ord(data[38])

        num_attributes = ord(data[39])
        if num_attributes == 0:
            self.extended_attributes = None
        else:
            self.extended_attributes = {}
            for i in xrange(num_attributes):
                k = self._decode_string(mbdb)
                v = self._decode_data(mbdb)
                self.extended_attributes[k] = v

    def _decode_string(self, s):
        s_len, = unpack('>H', s.read(2))
        if s_len == 0xffff:
            return None
        return s.read(s_len)

    def _decode_data(self, s):
        return self._decode_string(s)

    def type(self):
        return self.mode & 0xf000

    def is_symbolic_link(self):
        return self.type() == MASK_SYMBOLIC_LINK

    def is_regular_file(self):
        return self.type() == MASK_REGULAR_FILE

    def is_directory(self):
        return self.type() == MASK_DIRECTORY

class MBDB(object):
    def __init__(self, path):
        self.files = {}

        # open the index
        mbdx = file(path + '/Manifest.mbdx', 'rb')

        # skip signature
        signature = mbdx.read(len(MBDX_SIGNATURE))
        if signature != MBDX_SIGNATURE:
            raise Exception("Bad mbdx signature")

        # open the database
        mbdb = file(path + '/Manifest.mbdb', 'rb')

        # skip signature
        signature = mbdb.read(len(MBDB_SIGNATURE))
        if signature != MBDB_SIGNATURE:
            raise Exception("Bad mbdb signature")

        # number of records in mbdx
        records, = unpack('>L', mbdx.read(4))

        for i in xrange(records):
            # get the fixed size mbdx record
            buf = mbdx.read(26)

            # convert key to text. it is the filename in the backup directory
            sb = buf[:20].encode('hex')
            if len(sb) % 2 == 1:
                sb = '0'+sb
            offset, = unpack('>L', buf[20:24])

            # read the record in the mbdb
            offset, = unpack('>L', buf[20:24])
            mbdb.seek(len(MBDB_SIGNATURE) + offset, os.SEEK_SET)

            rec = MBFileRecord(mbdb)
            self.files[sb] = rec

        mbdx.close()
        mbdb.close()

    def get_file_by_name(self, filename):
        for (k, v) in self.files.iteritems():
            if v.path == filename:
                return (k, v)
        return None

        '''
        for f in self.files:
            print f.path
        '''

def getBackupKeyBag(backupfolder, passphrase):
    manifest = BPlistReader.plistWithFile(backupfolder + "/Manifest.plist")

    kb = Keybag(manifest["BackupKeyBag"].data)

    if kb.unlockBackupKeybagWithPasscode(passphrase):
        print "BackupKeyBag unlock OK"
        return kb
    else:
        return None

def warn(msg):
    print "WARNING: %s" % msg

def main():
    if len(sys.argv) not in [3, 4]:
        print "Usage: %s <backup path> <output path> [password]" % sys.argv[0]
        sys.exit(1)

    backup_path = sys.argv[1]
    output_path = sys.argv[2]
    if len(sys.argv) == 4:
        password = sys.argv[3]
    else:
        password = ''

    mbdb = MBDB(backup_path)

    kb = getBackupKeyBag(backup_path, password)
    if kb is None:
        raise Exception("Cannot decrypt keybag. Wrong pass?")

    for record in mbdb.files.values():
        # create directories if they do not exist
        # makedirs throw an exception, my code is ugly =)
        if record.is_directory():
            try:
                os.makedirs(output_path + '/' + record.path)
            except:
                pass

    for (filename, record) in mbdb.files.items():
        # skip directories
        if record.is_directory():
            continue

        # adjust output file name
        if record.is_symbolic_link():
            out_file = record.target
        else:
            out_file = record.path

        # read backup file
        try:
            f = file(backup_path + '/' + filename, 'rb')
            file_data = f.read()
            f.close()
        except(IOError):
            warn("File %s (%s) has not been found" % (filename, record.path))
            continue

        if record.encryption_key is not None: # file is encrypted!
            if kb.classKeys.has_key(record.protection_class):
                kek = kb.classKeys[record.protection_class]['KEY']

                k = AESUnwrap(kek, record.encryption_key[4:])
                if k is not None:
                    c = AES.new(k, AES.MODE_CBC)
                    file_data = c.decrypt(file_data)

                    padding = file_data[record.size:]
                    if len(padding) > AES.block_size or padding != chr(len(padding)) * len(padding):
                        warn("Incorrect padding for file %s" % record.path)
                    file_data = file_data[:record.size]

                else:
                    warn("Cannot unwrap key")
                    continue
            else:
                warn("Cannot load encryption key for file %s" % f)

        # write output file
        print("Writing %s" % out_file)
        f = file(output_path + '/' + out_file, 'wb')
        f.write(file_data)
        f.close()
    pass

if __name__ == '__main__':
    main()
