#!/bin/bash

#any ipsw should work
URL="http://appldnld.apple.com/iPhone4/041-0551.20110325.Aw2Dr/iPhone3,1_4.3.1_8G4_Restore.ipsw"
IPSW="iPhone3,1_4.3.1_8G4_Restore.ipsw"
RAMDISK="038-0902-005.dmg"
CUSTOMRAMDISK="myramdisk.dmg"
IMG3FS="./img3fs/img3fs"
IMG3MNT="/tmp/img3"

if [ ! -f $IPSW ]; then
    curl -O $URL
fi

if [ ! -f $RAMDISK ]; then
    unzip $IPSW $RAMDISK
fi

if [ ! -f ssh.tar.gz ]; then
    curl -O http://iphone-dataprotection.googlecode.com/files/ssh.tar.gz
fi

mkdir $IMG3MNT

$IMG3FS $IMG3MNT $RAMDISK

hdiutil attach $IMG3MNT/DATA.dmg

#remove baseband files to free space
rm -rf /Volumes/ramdisk/usr/local/standalone/firmware/*
tar -C /Volumes/ramdisk/ -xP <  ssh.tar.gz

cp ramdisk_tools/restored_external /Volumes/ramdisk/usr/local/bin

cp ramdisk_tools/bruteforce ramdisk_tools/data_partition ramdisk_tools/dump_data_partition.sh /Volumes/ramdisk/var/root


hdiutil eject /Volumes/ramdisk
umount $IMG3MNT

mv $RAMDISK $CUSTOMRAMDISK