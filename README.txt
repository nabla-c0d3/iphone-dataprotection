http://code.google.com/p/iphone-dataprotection/wiki/README

Supported devices

The tools have been tested on :
    iPhone 3GS
    iPhone 4 GSM
They should work as well on :
    iPad 1
    iPhone 4 CDMA
    iPod touch 3G & 4G
Devices older than iPhone 3GS are not supported.

Requirements
    iOS 5.0 IPSW for the target device
        even if the target device runs iOS 4 (iOS 5 kernel is backward compatible)
    Mac OS X >= 10.6 : for builing the tools and ramdisk
        iOS SDK 4.x or 5.x
        ldid
        MacFUSE or OSXFuse
    Python : for building a custom kernel and computer-side tools
        pycrypto
        M2crypto
        construct
        progressbar
    redsn0w : for booting the ramdisk

Mac OS X is only required to build the custom ramdisk. Once this is done, Windows can be used to boot the ramdisk and interact with it, either through ssh or using the python scripts provided. Linux is not supported.

Installing dependencies (Mac OS X)

    curl -O http://networkpx.googlecode.com/files/ldid
    chmod +x ldid
    sudo mv ldid /usr/bin/

    #install OSXFuse for img3fs
    curl -O -L https://github.com/downloads/osxfuse/osxfuse/OSXFUSE-2.3.4.dmg
    hdiutil mount OSXFUSE-2.3.4.dmg
    sudo installer -pkg /Volumes/FUSE\ for\ OS\ X/Install\ OSXFUSE\ 2.3.pkg -target /
    hdiutil eject /Volumes/FUSE\ for\ OS\ X/

    #you will need these python modules on Windows as well
    sudo ARCHFLAGS='-arch i386 -arch x86_64' easy_install pycrypto
    sudo easy_install M2crypto construct progressbar

Mercurial (http://mercurial.selenic.com/) is also required to checkout the source code from the repository.

Building custom ramdisk & kernel (Mac OS X)

    hg clone https://code.google.com/p/iphone-dataprotection/ 
    cd iphone-dataprotection

    make -C img3fs/

    curl -O -L https://sites.google.com/a/iphone-dev.com/files/home/redsn0w_mac_0.9.9b5.zip
    unzip redsn0w_mac_0.9.9b5.zip
    cp redsn0w_mac_0.9.9b5/redsn0w.app/Contents/MacOS/Keys.plist .

    python python_scripts/kernel_patcher.py IOS5_IPSW_FOR_YOUR_DEVICE
        Decrypting kernelcache.release.n88
        Unpacking ...
        Doing CSED patch
        Doing getxattr system patch
        Doing _PE_i_can_has_debugger patch
        Doing IOAESAccelerator enable UID patch
        Doing AMFI patch
        Patched kernel written to kernelcache.release.n88.patched
        Created script make_ramdisk_n88ap.sh, you can use it to (re)build the ramdisk

    sh ./make_ramdisk_n88ap.sh

Using the ramdisk

The first step is to boot the ramdisk and custom kernel. This can be done easily on OSX or Windows using redsn0w (follow redsn0w instructions to put the device in DFU mode).

    ./redsn0w_mac_0.9.9b5/redsn0w.app/Contents/MacOS/redsn0w -i IOS5_IPSW_FOR_YOUR_DEVICE -r myramdisk.dmg -k kernelcache.release.n88.patched

If the process fails with the "No identifying data fetched" error, make sure that the host computer is connected to the internet.
After redsn0w is done, the ramdisk should boot in verbose mode. Once "OK" appears on the screen, the custom ramdisk has successfully started. The device is now accessible using ssh over usbmux. Use the following command to setup port redirections:

    #./tcprelay.sh
    python usbmuxd-python-client/tcprelay.py -t 22:2222 1999:1999

SSH is now accessible at localhost:2222.

    #if ~/.ssh/id_rsa.pub exists on the host, it was copied to the ramdisk so no password is required.
    #otherwise root password is alpine
    ssh -p 2222 root@localhost

Port 1999 is used by the demo_bruteforce.py script. It connects to the custom restored_external daemon on the ramdisk, collects basic device information (serial number, UDID, etc.), unique device keys (keys 0x835 and 0x89B), downloads the system keybag and tries to bruteforce the passcode (4 digits only). If the bruteforce is successfull it will also download the keychain database.

    python python_scripts/demo_bruteforce.py

The results are stored in a plist file named after the device's data parititon volume identifier (a folder named after the device UDID is also created). This plist file is required for the other python scripts to operate correctly. For instance, the keychain database contents can be displayed using keychain_tool.py.

    python python_scripts/keychain_tool.py -d UDID/keychain-2.db UDID/DATAVOLUMEID.plist

A shell script is provided to create a dd image of the data parititon, that will be placed in the device UDID directory.

    ./dump_data_partition.sh

The image file can be opend using the modified HFSExplorer that will decrypt the files "on the fly". To decrypt it permanently (for use with standard tools), the emf_decrypter.py script can be used. Both tools depends on the aforementioned plist file being in the same directory as the disk image.

    #do a dry run to avoid crashing halfway
    python python_scripts/emf_decrypter.py --nowrite UDID/data_DATE.dmg

    #if no errors then decrypt the image in place
    python python_scripts/emf_decrypter.py UDID/data_DATE.dmg

Finally, the HFS journal file can be carved to search for deleted files. Keep in mind that only a very few number of files (or even none at all) can be recovered that way.

    python python_scripts/emf_undelete.py UDID/data_DATE.dmg
