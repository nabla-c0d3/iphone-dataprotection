#!/bin/bash

set +e
set -o errexit

if [ $# -ne 4 ]
then
    echo "Syntax: $0 IPSW RAMDISK KEY IV"
    echo "python_scripts/kernel_patcher.py can generate a shell script with the correct parameters"
    exit
fi

IPSW=$1
RAMDISK=$2
KEY=$3
IV=$4
CUSTOMRAMDISK="myramdisk.dmg"
IMG3FS="./img3fs/img3fs"
IMG3MNT="/tmp/img3"

if [ ! -f $IMG3FS ]; then
    echo "img3fs is missing, install osxfuse and run make -C img3fs/"
    exit -1
fi

if [ ! -f ssh.tar.gz ]; then
    echo "Downloading ssh.tar.gz from googlecode"
    curl -O http://iphone-dataprotection.googlecode.com/files/ssh.tar.gz
fi

unzip $IPSW $RAMDISK

mkdir -p $IMG3MNT

$IMG3FS -key $KEY -iv $IV $IMG3MNT $RAMDISK

hdiutil attach $IMG3MNT/DATA.dmg

#remove baseband files to free space
rm -rf /Volumes/ramdisk/usr/local/standalone/firmware/*
rm -rf /Volumes/ramdisk/usr/share/progressui/
tar -C /Volumes/ramdisk/ -xzP <  ssh.tar.gz
rm /Volumes/ramdisk/bin/vdir
rm /Volumes/ramdisk/bin/egrep
rm /Volumes/ramdisk/bin/grep

cp ramdisk_tools/restored_external /Volumes/ramdisk/usr/local/bin

cp ramdisk_tools/bruteforce ramdisk_tools/device_infos /Volumes/ramdisk/var/root
cp ramdisk_tools/scripts/* /Volumes/ramdisk/var/root

#if present, copy ssh public key to ramdisk
if [ -f ~/.ssh/id_rsa.pub ]; then
	mkdir /Volumes/ramdisk/var/root/.ssh
	cp ~/.ssh/id_rsa.pub /Volumes/ramdisk/var/root/.ssh/authorized_keys
fi

hdiutil eject /Volumes/ramdisk
umount $IMG3MNT

mv $RAMDISK $CUSTOMRAMDISK

echo "$CUSTOMRAMDISK created"

