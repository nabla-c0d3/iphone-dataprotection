compile img3fs (requires MacFUSE)
compile cyanide payload
compile modified tetherboot from syringe folder
build ramdisk (requires ssh.tar.gz and img3fs)
boot ramdisk using : tetherboot.exe -p cyanide_bootramdisk\payload -r myramdisk.dmg