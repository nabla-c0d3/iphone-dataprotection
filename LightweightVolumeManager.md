# Description #

LightweightVolumeManager is a volume manager kernel extension introduced in iOS 5 (com.apple.driver.LightweightVolumeManager kext).
It allows resizing of the partitions (used to create the OTA update partition), and handles the volume encryption key for the data partition (replacing EffacingMediaFilter).
LwVM splits the logical disk in chunks (1024 chunks at most).
Each chunk is mapped to one partition. Chunks of the same partition are not necessarily contiguous.

LwVM wraps the default block device (disk0), and publishes a media (disk0s1) with a "fake" GPT partition table that is then matched by IOGUIDPartitionScheme.

```
    | |   |       | +-o AppleNANDLegacyFTL
    | |   |       |   +-o IOFlashBlockDevice
    | |   |       |   | +-o IOBlockStorageDriver
    | |   |       |   |   +-o unknown vendor unknown product Media  (IOMedia)
    | |   |       |   |     +-o IOMediaBSDClient              /dev/disk0
    | |   |       |   |     +-o LightweightVolumeManager
    | |   |       |   |       +-o IOMedia@1                   /dev/disk0s1
    | |   |       |   |         +-o IOMediaBSDClient
    | |   |       |   |         +-o IOGUIDPartitionScheme
    | |   |       |   |           +-o System@1  (IOMedia)
    | |   |       |   |           | +-o IOMediaBSDClient      /dev/disk0s1s1
    | |   |       |   |           +-o Data@2  (IOMedia)
    | |   |       |   |             +-o IOMediaBSDClient      /dev/disk0s1s2
```

Reads and write to the fake GPT are trapped by the LwVM driver : modification of the GPT by userland tools triggers repartitionning by LwVM. Internally, the LwVM partition table and chunk map are stored on the "real" block device (disk0), in the first chunk (which is reserved).

```
//https://github.com/iDroid-Project/openiBoot/blob/master/includes/bdev.h
typedef struct _LwVMPartitionRecord {
	uint64_t type[2];
	uint64_t guid[2];
	uint64_t begin;
	uint64_t end;
	uint64_t attribute; // 0 == unencrypted; 0x1000000000000 == encrypted
	char	partitionName[0x48];
} __attribute__ ((packed)) LwVMPartitionRecord;

typedef struct _LwVM {
	uint64_t type[2];
	uint64_t guid[2];
	uint64_t mediaSize;
	uint32_t numPartitions;
	uint32_t crc32;
	uint8_t unkn[464];
	LwVMPartitionRecord partitions[12];
	uint16_t chunks[1024]; // chunks[0] should be 0xF000
} __attribute__ ((packed)) LwVM;
```

# LwVM effaceable locker #

LwVM allows multiple partitions to be encrypted (up to a maximum of 9 keys). Like EffacingMediaFilter on iOS 4, encryption keys are encrypted by key 0x89B and stored in the effaceable area ('LwVM' locker).

```
struct LwVMPartitionKey
{
	uint8_t uuid[16];
	uint8_t key[32];
};

//'LwVM' locker in effaceable storage
struct LwVMKeyBag
{
	uint8_t random[12];
	uint32_t num_keys;
	uint8_t media_uuid[16];
	struct LwVMPartitionKey keys[1];//num_keys entries
};

```

A partition is encrypted when the kLwVMAttributeEncrypted flag (0x1000000000000) is set in its GPT entry ent\_attr field. This flag is mirrored into the LwVM partition table.

# References #

  * https://github.com/iDroid-Project/openiBoot/blob/master/includes/bdev.h