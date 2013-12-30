#!/bin/bash

if [ ! $(uname) == "Darwin" ]
then
    echo "Script for Mac OS X only"
    exit
fi

if [ $# -lt 1 ]
then
    echo "Syntax: $0 DECRYPTED_RAMDISK_DMG"
    exit
fi

if [ ! -f ssh.tar.gz ]
then
    echo "Downloading ssh.tar.gz from googlecode"
    curl -O http://iphone-dataprotection.googlecode.com/files/ssh.tar.gz
fi

if [ ! -f libncurses.5.dylib ]
then
    echo "Downloading libncurses.5.dylib from googlecode"
    curl -O http://iphone-dataprotection.googlecode.com/files/libncurses.5.dylib
fi

echo "Rebuilding ramdisk_tools"

./build_tools.sh

#compiling in a vmware shared folder can produce binaries filled with zeroes !
if [ ! -f ramdisk_tools/restored_external ] || [ "$(file -b ramdisk_tools/restored_external)" == "data" ]
then
    echo "ramdisk_tools/restored_external not found or invalid, check compilation output for errors"
    exit -1
fi

RAMDISK=$1

RD_SIZE=$(du -h $RAMDISK  | cut -f 1)

if [ ! $RD_SIZE == "20M" ]
then
    echo "resizing ramdisk..."
    echo "hdiutil will segfault if ramdisk was already resized, thats ok"
    hdiutil resize -size 20M $RAMDISK
fi

if [ -d /Volumes/ramdisk ]
then
    echo "Unmount /Volumes/ramdisk then try again"
    exit -1
fi

echo "Attaching ramdisk"

hdiutil attach $RAMDISK
rm -rf /Volumes/ramdisk/usr/local/standalone/firmware/*
rm -rf /Volumes/ramdisk/usr/share/progressui/

if [ ! -f /Volumes/ramdisk/sbin/sshd ]
then
    echo "Unpacking ssh.tar.gz on ramdisk..."
    tar -C /Volumes/ramdisk/ -xzkP <  ssh.tar.gz
    echo "^^ This tar error message is okay"
fi

if [ ! -f /Volumes/ramdisk/usr/lib/libncurses.5.4.dylib ]
then
    echo "Adding libncurses..."
    cp libncurses.5.dylib /Volumes/ramdisk/usr/lib/libncurses.5.4.dylib
fi

echo "Adding/updating ramdisk_tools binaries on ramdisk..."
cp ramdisk_tools/restored_external /Volumes/ramdisk/usr/local/bin/
cp ramdisk_tools/bruteforce ramdisk_tools/device_infos /Volumes/ramdisk/var/root
cp ramdisk_tools/scripts/* /Volumes/ramdisk/var/root

ls -laht /Volumes/ramdisk/usr/local/bin/

#if present, copy ssh public key to ramdisk
if [ -f ~/.ssh/id_rsa.pub ] && [ ! -d /Volumes/ramdisk/var/root/.ssh ]
then
    mkdir /Volumes/ramdisk/var/root/.ssh
    cp ~/.ssh/id_rsa.pub /Volumes/ramdisk/var/root/.ssh/authorized_keys
    chmod 0600 /Volumes/ramdisk/var/root/.ssh/authorized_keys
fi

hdiutil eject /Volumes/ramdisk
