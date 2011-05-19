import hashlib,struct,glob,sys,os
from crypto.PBKDF2 import PBKDF2
from util.bplist import BPlistReader
from Crypto.Cipher import AES
from util import read_file, write_file
import plistlib

"""
decrypt iOS 3 backup blob (metadata and file contents)
"""

def decrypt_blob(blob, auth_key):
    len = struct.unpack(">H", blob[0:2])[0]
    if len != 66:
        print "blob len != 66"
    magic = struct.unpack(">H", blob[2:4])[0]
    if magic != 0x0100:
        print "magic != 0x0100"
    iv = blob[4:20]
    
    blob_key = AES.new(auth_key, AES.MODE_CBC, iv).decrypt(blob[20:68])[:32]

    return AES.new(blob_key, AES.MODE_CBC, iv).decrypt(blob[68:])

def decrypt_backup(backupfolder, outputfolder, passphrase):

    manifest = plistlib.readPlist(backupfolder + "/Manifest.plist")
        
    if not manifest["IsEncrypted"]:
        print "backup is not encrypted manifest[IsEncrypted]"
        return

    manifest_data = manifest["Data"].data

    authdata = manifest["AuthData"].data

    pkbdf_salt = authdata[:8]
    iv = authdata[8:24]
    key = PBKDF2(passphrase,pkbdf_salt,iterations=2000).read(32)

    data = AES.new(key, AES.MODE_CBC, iv).decrypt(authdata[24:])
    auth_key = data[:32]

    if hashlib.sha1(auth_key).digest() != data[32:52]:
        print "wrong auth key (hash mismatch) => wrong passphrase"
        return

    print "Passphrase seems OK"

    for mdinfo_name in glob.glob(backupfolder + "/*.mdinfo"):

        mddata_name = mdinfo_name[:-7] + ".mddata"
        mdinfo = BPlistReader.plistWithFile(mdinfo_name)

        if mdinfo["IsEncrypted"]:
            metadata = decrypt_blob(mdinfo["Metadata"], auth_key)
            metadata = BPlistReader.plistWithString(metadata)
            
            print metadata["Path"]        
            
            filedata = read_file(mddata_name)
            filedata = decrypt_blob(filedata, auth_key)
            
            filename = metadata["Path"].replace("/","_")
            
            write_file(outputfolder + "/" + filename, filedata)