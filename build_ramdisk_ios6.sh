#!/bin/bash

if [ $# -lt 1 ]
then
    echo "Syntax: $0 DECRYPTED_RAMDISK_DMG"
    exit
fi

if [ ! -f ramdisk_tools/restored_external ]
then
    echo "ramdisk_tools/restored_external not found, check compilation output for errors"
    exit -1
fi

if [ ! -f ssh.tar.gz ]; then
    echo "Downloading ssh.tar.gz from googlecode"
    curl -O http://iphone-dataprotection.googlecode.com/files/ssh.tar.gz
fi

if [ ! -f libncurses.5.dylib ]; then
    echo "Downloading libncurses.5.dylib from googlecode"
    curl -O http://iphone-dataprotection.googlecode.com/files/libncurses.5.dylib
fi

RAMDISK=$1

#hdiutil will segfault if ramdisk was already resized, thats ok
hdiutil resize -size 30M $RAMDISK

hdiutil attach $RAMDISK
rm -rf /Volumes/ramdisk/usr/local/standalone/firmware/*
rm -rf /Volumes/ramdisk/usr/share/progressui/

tar -C /Volumes/ramdisk/ -xzkP <  ssh.tar.gz

#ioflashstoragekit not compatible with ios6

cp ramdisk_tools/restored_external /Volumes/ramdisk/usr/local/bin/
cp ramdisk_tools/bruteforce ramdisk_tools/device_infos /Volumes/ramdisk/var/root
cp ramdisk_tools/scripts/* /Volumes/ramdisk/var/root

cp libncurses.5.dylib /Volumes/ramdisk/usr/lib/libncurses.5.4.dylib

#if present, copy ssh public key to ramdisk
if [ -f ~/.ssh/id_rsa.pub ]; then
    mkdir /Volumes/ramdisk/var/root/.ssh
    cp ~/.ssh/id_rsa.pub /Volumes/ramdisk/var/root/.ssh/authorized_keys
fi

hdiutil eject /Volumes/ramdisk
