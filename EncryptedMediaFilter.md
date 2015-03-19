iOS 3 data partition encryption layer.

The entire data partition is encrypted using a single key (media key or EMF key), stored encrypted by key 0x89B in the partition last logical block. There is no per-file encryption. The MBR partition type is 0xAE (Apple Encrypted).

```
struct crpt_ios3
{
    uint32_t magic0; //'tprc'
    struct encryted_data //encrypted with key89b CBC mode zero iv
    {
        uint32_t magic1; // 'TPRC'
        uint64_t partition_size_in_bytes; //?
        uint32_t unknown;//0xFFFFFFFF
        uint8_t filesystem_key[32]; //EMF key
        uint32_t key_length; //=32
        uint32_t pad_zero[3];
    };
};
```

## crpt\_ios3 structure hexdump ##

```
00000000 | 74 70 72 63 0F D4 BA 64 07 C5 37 B0 57 1F EF 0C | tprc...d..7.W...
00000010 | F2 73 82 B2 03 BC B3 AE 8E 89 A1 A7 58 5F F8 45 | .s..........X_.E
00000020 | 7D DF 0E 28 94 0D FB F5 70 C5 B0 1E 3A 14 31 08 | }..(....p...:.1.
00000030 | A9 89 FC 8B 07 B9 1F 3C 79 AE 0C 4D AC C1 DA 88 | .......<y..M....
00000040 | 70 4C A3 BC 00 00 00 00 00 00 00 00 00 00 00 00 | pL..............
```

## encryted\_data structure hexdump (after decryption) ##

```
00000000 | 54 50 52 43 00 40 CA 9A 03 00 00 00 FF FF FF FF | TPRC.@..........
00000010 | 3A C7 5B 6A 3E 6C 05 DC A2 DC 5E 90 9A 07 2E 1E | :.[j>l....^.....
00000020 | 81 C9 95 E3 E8 1B D7 E8 0C 6B 0F 4B 0D 8D 9E 55 | .........k.K...U
00000030 | 20 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 |  ...............
```

# iOS 3.x wipe vulnerability #

When a data partition wipe is triggered on iOS 3.x, the last logical block containing the EMF key is overwritten with a new one, but only at the block device level, so the old NAND page is not erased immediatly. This means that if a NAND dump is acquired right after the wipe operation occured, it is still possible to recover the wiped EMF key, and reconstruct the old data partition.

```
$./ios3_unwipe.py iphone3gs_ios3_wipe.bin iphone3gs_ios3_wipe.plist
Partition   Start LBA   End LBA     Size
0           63          96063       750MB
1           96075       1967805     14GB
Data partition was wiped (/root/.obliterated)
Found 3 versions for logical page 1967804
-----------------------------------------------------------------------------
USN: 1041045
00000000 | 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 | ................
00000010 | 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 | ................
00000020 | 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 | ................
00000030 | 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 | ................
00000040 | 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 | ................
-----------------------------------------------------------------------------
USN: 1041046
00000000 | 74 70 72 63 F8 47 DE 10 E1 BA ED 20 37 BD 04 E6 | tprc.G..... 7...
00000010 | 05 B6 E9 71 67 55 EA 85 7F 4C 6E 6F E4 55 3B 64 | ...qgU...Lno.U;d
00000020 | 0D 6C AB 3F C2 62 46 68 A1 DD 71 A9 C0 6E EE 1B | .l.?.bFh..q..n..
00000030 | 03 CD 1A C4 6F 29 2C 0A 96 98 B9 70 3D DC FD DA | ....o),....p=...
00000040 | 3F 05 D3 6E 00 00 00 00 00 00 00 00 00 00 00 00 | ?..n............
EMF key = 01f797f7d4576e4995c4f08e836552fcdc307cea90bfb0976bbcd89c05b66b87
-----------------------------------------------------------------------------
USN: 1041396
00000000 | 74 70 72 63 F8 47 DE 10 E1 BA ED 20 37 BD 04 E6 | tprc.G..... 7...
00000010 | 05 B6 E9 71 AF 96 37 81 A7 0A CA 06 A1 FF 77 74 | ...q..7.......wt
00000020 | BB AF 00 BF 5F 27 82 7F CC F9 B8 22 91 E6 BD E9 | ...._'....."....
00000030 | E3 36 FE 11 8D 82 18 01 B2 A4 F1 BC D4 2F 9B E1 | .6.........../..
00000040 | E8 BA D5 09 00 00 00 00 00 00 00 00 00 00 00 00 | ................
EMF key = 5dd24b50aa2517c258ed9fab46b39ad23fc78be63c6344fe93c25e8db38b26a0
```

This vulnerability was fixed in iOS 4 with EffacingMediaFilter.