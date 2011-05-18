CC=/Developer/Platforms/iPhoneOS.platform/Developer/usr/bin/arm-apple-darwin10-gcc-4.0.1 
CFLAGS=-Wall -arch armv6 -isysroot /Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS4.2.sdk/
CFLAGS_IOKIT=$(CFLAGS) -I/usr/local/include -framework IOKit -framework CoreFoundation -framework Security -O3 -F/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS4.2.sdk/System/Library/PrivateFrameworks/ -framework IOMobileFrameBuffer -framework CoreGraphics -framework CoreSurface -framework ImageIO

all: IOUSBDeviceControllerLib.h data_partition restored_external bruteforce

IOUSBDeviceControllerLib.h:
	curl -o IOUSBDeviceControllerLib.h http://www.opensource.apple.com/source/IOKitUser/IOKitUser-502/usb_device.subproj/IOUSBDeviceControllerLib.h?txt


data_partition: data_partition.c device_info.c IOAESAccelerator.c AppleEffaceableStorage.c AppleKeyStore.c bsdcrypto/pbkdf2.c bsdcrypto/sha1.c bsdcrypto/key_wrap.c bsdcrypto/rijndael.c util.c IOKit.c registry.c
	$(CC) $(CFLAGS_IOKIT) -o $@ $^
	ldid -S $@

restored_external: restored_external.c device_info.c remote_functions.c plist_server.c AppleKeyStore.c AppleEffaceableStorage.c IOKit.c IOAESAccelerator.c util.c registry.c AppleKeyStore_kdf.c bsdcrypto/pbkdf2.c bsdcrypto/sha1.c bsdcrypto/rijndael.c bsdcrypto/key_wrap.c
	$(CC) $(CFLAGS_IOKIT) -o $@ $^
	ldid -Skeystore_device.xml $@

bruteforce: systemkb_bruteforce.c AppleKeyStore.c AppleEffaceableStorage.c IOKit.c IOAESAccelerator.c util.c registry.c AppleKeyStore_kdf.c bsdcrypto/pbkdf2.c bsdcrypto/sha1.c bsdcrypto/rijndael.c bsdcrypto/key_wrap.c image.c
	$(CC) $(CFLAGS_IOKIT) -o $@ $^
	ldid -S $@
	ldid -Skeystore_device.xml $@

rebuild: clean all
