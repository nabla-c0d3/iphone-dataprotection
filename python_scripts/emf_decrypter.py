from optparse import OptionParser
from hfs.emf import EMFVolume

def main():
    parser = OptionParser(usage="emf_decrypter.py disk_image.bin")
    parser.add_option("-w", "--nowrite", dest="write", action="store_false", default=True,
                  help="disable modifications of input file, for testing")
    (options, args) = parser.parse_args()
    if len(args) < 1:
        parser.print_help()
        return
    v = EMFVolume(args[0], write=options.write)
    if options.write:
        print "WARNING ! This tool will modify the hfs image and possibly wreck it if something goes wrong !"
        print "Make sure to backup the image before proceeding"
        print "You can use the --nowrite option to do a dry run instead"
    else:
        print "Test mode : the input file will not be modified"
    print "Press a key to continue or CTRL-C to abort"
    raw_input()
    v.decryptAllFiles()

if __name__ == "__main__": 
    main()
