import plistlib
import sys
from optparse import OptionParser
from keystore.keybag import Keybag
from keychain import keychain_load
from keychain.managedconfiguration import bruteforce_old_pass

def main():
    parser = OptionParser(usage="%prog keychain.db keyfile.plist")
    parser.add_option("-d", "--display", dest="display", action="store_true", default=False,
                  help="Show keychain items on stdout")
    parser.add_option("-s", "--sanitize", dest="sanitize", action="store_true", default=False,
                  help="Hide secrets on stdout with ***")
    parser.add_option("-p", "--passwords", dest="passwords", action="store_true", default=False,
                  help="Save generic & internet passwords as CSV file")
    parser.add_option("-c", "--certs", dest="certs", action="store_true", default=False,
                  help="Extract certificates and keys")
    parser.add_option("-o", "--old", dest="oldpass", action="store_true", default=False,
                  help="Bruteforce old passcodes")
    
    (options, args) = parser.parse_args()
    if len(args) < 2:
        parser.print_help()
        return
    
    p = plistlib.readPlist(args[1])
    kb = Keybag.createWithPlist(p)
    k = keychain_load(args[0], kb, p["key835"].decode("hex"))
    
    if options.display:
        k.print_all(options.sanitize)
    if options.passwords:
        k.save_passwords()
    if options.certs:
        k.save_certs_keys()

    if options.oldpass:
        mc = k.get_managed_configuration()
        if not mc:
            print "Managed configuration not found"
            return
        print "Bruteforcing %d old passcodes" % len(mc.get("history",[]))
        for h in mc["history"]:
            p = bruteforce_old_pass(h)
            if p:
                print "Found : %s" % p
            else:
                print "Not Found"

if __name__ == "__main__": 
    main()
