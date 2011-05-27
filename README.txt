compile img3fs (requires MacFUSE)
compile cyanide payload
compile modified tetherboot from syringe folder
compile ramdisk_tools
    create symlink for IOKit headers (change iPhoneOS4.2.sdk to match your sdk version)
    sudo ln -s /System/Library/Frameworks/IOKit.framework/Versions/Current/Headers /Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS4.2.sdk/System/Library/Frameworks/IOKit.framework/Headers 
    
build ramdisk (requires ssh.tar.gz and img3fs)
boot ramdisk using : tetherboot.exe -p cyanide_bootramdisk\payload -r myramdisk.dmg