# Description #

Per file encryption extension added to the HFS filesystem in iOS 4. Each file gets a unique file key used to encrypt its data fork. File keys are stored (wrapped) in an extended attribute named **com.apple.system.cprotect**.

Wrapping/unwrapping is handled by the AppleKeyStore kernel extension.

Content protection code is present in the open source version of the xnu kernel, but not used on desktop OSX.

http://opensource.apple.com/source/xnu/xnu-1699.24.8/bsd/hfs/hfs_cprotect.c

http://opensource.apple.com/source/xnu/xnu-1699.24.8/bsd/sys/cprotect.h

# Extended attribute format #

```
#define CP_WRAPPEDKEYSIZE  40

/*
 * On-disk structure written as the per-file EA payload 
 * All on-disk multi-byte fields for the CP XATTR must be stored
 * little-endian on-disk.  This means they must be endian swapped to
 * L.E on getxattr() and converted to LE on setxattr().	
 */
struct cp_xattr {
	u_int16_t	xattr_major_version;
	u_int16_t	xattr_minor_version;
	u_int32_t	flags;
	u_int32_t	persistent_class;
	u_int32_t	key_size;
	//20 bytes of padding (?) here when xattr_major_version == 4 (iOS >= 5)
	uint8_t		persistent_key[CP_WRAPPEDKEYSIZE];	
};
```

# References #

**[US20110252234 - System and method for file-level data protection](https://www.google.com/patents/US20110252234)**
