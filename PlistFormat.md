| **Field** | **Type** | **Description** |
|:----------|:---------|:----------------|
| DKey  | hex string | Unwrapped [NSProtectionNone](EncryptionKeys.md) class key, all 00s when [nand-disable-driver](BootFlags.md) is set on NAND-only devices |
| EMF  | hex string | Decrypted [EMF](EncryptionKeys.md) key, all 00s when [nand-disable-driver](BootFlags.md) is set on NAND-only devices |
| btMac  | string | Bluetooth MAC address |
| wifiMac  | string  | Wi-Fi MAC address |
| serialNumber  | string | Serial Number |
| imei  | string  | IMEI for devices with a BaseBand |
| hwModel  | string  | Hardware model (ex N90AP for iphone 4) |
| udid  | string | Computed UDID |
| kern.bootargs | string | Ramdisk boot arguments (through sysctl) |
| key835 | hex string | Computed key835, all 00s if IOAESAccelerator UID kernel patch is missing |
| key89A | hex string | Computed key89A, all 00s if IOAESAccelerator UID kernel patch is missing |
| key89B | hex string | Computed key89B, all 00s if IOAESAccelerator UID kernel patch is missing |
| dataVolumeOffset | integer | Data partition first LBA, 0 when [nand-disable-driver](BootFlags.md) is set |
| dataVolumeUUID | hex string | Data partition UUID, 0 when [nand-disable-driver](BootFlags.md) is set |
| lockers  | data | Effaceable lockers read through [AppleEffaceableStorage](EffaceableArea.md) getBytes selector, unavailable when [nand-disable-driver](BootFlags.md) is set on NAND-only devices |
| KeyBagKeys  | data | System keybag decrypted payload, unavailable when [nand-disable-driver](BootFlags.md) is set |
| passcode  | string | Bruteforced passcode |
| passcodeKey  | hex string | Computed passcode key |
| classKeys | dictionary | Decrypted class keys (dictionary integer->hex string)|
| nand | dictionary | NAND parameters |

# NAND parameters #

| **Field** | **Type** | **Description** |
|:----------|:---------|:----------------|
| #ce | integer | Number of CEs |
| #ce-blocks | integer | Numbler of blocks per CE |
| #block-pages | integer | Number of pages per block |
| #page-bytes | integer | Page size |
| #spare-bytes | integer | Spare area size |
| dumpedPageSize | integer | ioflashstoragekit parameter, currently #page-bytes + meta-per-logical-page + 8 |
| #bootloader-bytes | integer | Bootloader pages size (currently 1536) for NAND-only devices |
| device-readid | integer | NAND device identifier |
| vendor-type | integer | NAND vendor identifier |
| meta-per-logical-page | integer |  |
| valid-meta-per-logical-page | integer |  |
| bbt-format | integer |  |
| banks-per-ce | integer | Number of virtual banks for VSVFL, default value (1) when [nand-disable-driver](BootFlags.md) is used |
| boot-from-nand | data | 32 bit integer as data |
| metadata-whitening | data | 32 bit integer as data  |