#!/usr/bin/python

import glob, os,sys

if sys.platform == "darwin":
    REDSNOW_PATH = "redsn0w_mac_0.9.15b3/redsn0w.app/Contents/MacOS/redsn0w"
else:
    REDSNOW_PATH = "redsn0w_win_0.9.15b3\\redsn0w.exe"

#return list of (ipsw,kernel,ramdisk)
def list_bootable():
    res = []
    for ipsw in glob.glob("data/ipsw/*.ipsw"):
        ipsw_id = os.path.basename(ipsw).replace("_Restore.ipsw", "")
        kernel = os.path.join("data", "boot", "kernel_%s.patched" % ipsw_id)
        ramdisk = os.path.join("data", "boot", "ramdisk_%s.dmg" % ipsw_id)
        
        if os.path.exists(kernel) and os.path.exists(ramdisk):
            res.append((ipsw, kernel, ramdisk))
    return res

def main():
    if not os.path.exists(REDSNOW_PATH):
        print "Extract %s in current directory" % REDSNOW_PATH.split(os.sep)[0]
        return 

    l = list_bootable()
    
    if len(l) == 0:
        print "Nothing to boot, run ./build.py"
        return
    elif len(l) == 1:
        ipsw, kernel, ramdisk = l[0]
    else:
        print "Choose IPSW :"
        for i in xrange(len(l)):
            print "[%d] %s" % (i+1, os.path.basename(l[i][0]))
        while True:
            x = raw_input("> ")
            if x.isdigit():
                x = int(x)
                if x > 0 and (x-1) < len(l):
                    ipsw, kernel, ramdisk = l[x-1]
                    break
            print "Invalid choice"

    print "Using %s" % ipsw
    #cs_enforcement_disable=1
    bootargs = "-v rd=md0 amfi=0xff msgbuf=409600"

    if raw_input("Use nand-disable boot flag ? [y/n] ") == "y":
        bootargs += " nand-disable=1"

    cmdline = "%s -i %s -k %s -r %s -a \"%s\"" % (REDSNOW_PATH, ipsw, kernel, ramdisk, bootargs)

    print "Boot args: %s" % bootargs
    print "Command line: %s" % cmdline
    print "Launching redsn0w..."
    os.system(cmdline)

if __name__ == "__main__":
    main()
