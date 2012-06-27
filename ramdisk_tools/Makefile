SDKVER?=5.1
SDK=/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS$(SDKVER).sdk/
CC:=$(wildcard /Developer/Platforms/iPhoneOS.platform/Developer/usr/bin/arm-apple-darwin10-*gcc*)
HGVERSION:= $(shell hg parents --template '{node|short}' || echo "unknown")
CFLAGS=-Wall -isysroot $(SDK) -DHGVERSION="\"${HGVERSION}\""
CFLAGS_IOKIT=$(CFLAGS) -framework IOKit -framework CoreFoundation -framework Security -O3 -I.

all: IOKit IOUSBDeviceControllerLib.h device_infos restored_external bruteforce ioflashstoragekit

IOUSBDeviceControllerLib.h:
	curl -o IOUSBDeviceControllerLib.h http://www.opensource.apple.com/source/IOKitUser/IOKitUser-502/usb_device.subproj/IOUSBDeviceControllerLib.h?txt

IOKit:
	ln -s /System/Library/Frameworks/IOKit.framework/Versions/Current/Headers IOKit

device_infos: device_infos.c device_info.c IOAESAccelerator.c AppleEffaceableStorage.c AppleKeyStore.c bsdcrypto/pbkdf2.c bsdcrypto/sha1.c bsdcrypto/key_wrap.c bsdcrypto/rijndael.c util.c IOKit.c registry.c ioflash/ioflash.c kernel_patcher.c
	$(CC) $(CFLAGS_IOKIT) -o $@ $^
	ldid -Stfp0.plist $@

restored_external: restored_external.c device_info.c remote_functions.c plist_server.c AppleKeyStore.c AppleEffaceableStorage.c IOKit.c IOAESAccelerator.c util.c registry.c AppleKeyStore_kdf.c bsdcrypto/pbkdf2.c bsdcrypto/sha1.c bsdcrypto/rijndael.c bsdcrypto/key_wrap.c ioflash/ioflash.c kernel_patcher.c
	$(CC) $(CFLAGS_IOKIT) -o $@ $^
	ldid -Skeystore_device.xml $@

bruteforce: systemkb_bruteforce.c AppleKeyStore.c AppleEffaceableStorage.c IOKit.c IOAESAccelerator.c util.c registry.c AppleKeyStore_kdf.c bsdcrypto/pbkdf2.c bsdcrypto/sha1.c bsdcrypto/rijndael.c bsdcrypto/key_wrap.c device_info.c ioflash/ioflash.c kernel_patcher.c
	$(CC) $(CFLAGS_IOKIT) -o $@ $^
	ldid -Skeystore_device.xml $@

ioflashstoragekit: ioflash/ioflash.c ioflash/ioflash_kernel.c ioflash/ioflashstoragekit.c util.c
	$(CC) $(CFLAGS_IOKIT) -o $@ $^
	ldid -Stfp0.plist $@

kernel_patcher: kernel_patcher.c
	$(CC) $(CFLAGS_IOKIT) -o $@ $^
	ldid -Stfp0.plist $@

shsh_dump: ioflash/ioflash.c ioflash/ioflash_kernel.c shsh_dump.c util.c
	$(CC) $(CFLAGS_IOKIT) -o $@ $^
	ldid -Stfp0.plist $@

clean:
	rm -f bruteforce restored_external device_infos ioflashstoragekit shsh_dump

rebuild: clean all
