import sys
from hfs.emf import EMFVolume

if __name__ == "__main__": 
    if len(sys.argv) < 2:
        print "Usage: emf_decrypter.py disk_image.bin"
        sys.exit(0)
    v = EMFVolume(sys.argv[1], write=True)
    print "WARNING ! This tool will modify the hfs image and possibly wreck it if something goes wrong !"
    print "Make sure to backup the image before proceeding"
    print "Press a key to continue or CTRL-C to abort"
    raw_input()
    v.decryptAllFiles()