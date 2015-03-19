The effaceable area was introduced in iOS 4 to store small blobs of data (lockers) that can be erased securely. It is used to store encryption keys for the filesystem and the system keybag.

On NAND-only devices, this area is located in the plog partition, and not subject to any kind of translation (FTL/VFL). On older devices, it is located at offset 0xFA000 in NOR.

The effaceable area is composed of multiple "units" that contain the same lockers data for redundancy. Each unit starts with a 64-bytes header followed by 960 bytes used to store the lockers data.

# Header Format #

```
header[0:16] XOR header[16:32] = magic = 'ecaF' + 0x1 + 0x1 + 0x0
header[0x38:0x38+4] = generation (number of erase/write cycles)
header[0x3C:0x40] = crc32(lockers[:960], crc32(header[0x20:0x3C], crc32(magic)))
```

# Lockers format #

| 'kL' | length (word) | tag | data (length) |
|:-----|:--------------|:----|:--------------|

Bit 31 of tag field marks protected lockers (not accessible from userland)

# iOS 4 lockers #

| Tag | Protected | Length | Contents |
|:----|:----------|:-------|:---------|
| EMF! | yes | 0x24| length (0x20) + AES(key89B, emf\_key) |
| DKey | yes | 0x28 | AESWRAP(key835, NSProtectionNone\_classkey) |
| BAG1 | no | 0x34 | 'BAG1' + IV + Key |
| DONE | - | 0 | empty "sentinel" trailing locker |

# AppleEffaceableStorage IOKit userland interface #

| Selector | Description | Comment |
|:---------|:------------|:--------|
| 0 | getCapacity | 960 bytes |
| 1 | getBytes | requires PE\_i\_can\_has\_debugger |
| 2 | setBytes | requires PE\_i\_can\_has\_debugger |
| 3 | isFormatted |  |
|  4 | format  |  |
| 5 | getLocker | input : locker tag, output : data |
| 6 | setLocker | input : locker tag, data |
| 7 | effaceLocker | input : locker tag |
| 8 | lockerSpace | ? |