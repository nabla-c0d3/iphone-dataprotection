# Description (see [issue 19](https://code.google.com/p/iphone-dataprotection/issues/detail?id=19)) #
On iOS 4, when the security epoch stored in the [NANDDRIVERSIGN](NANDDRIVERSIGN.md) special pages differs from the one returned by the `_PE_get_security_epoch` function (that returns a static value for the current kernel), the `WMR_Init` function initiates an epoch update.

The kernel tries to update the block containing the [NANDDRIVERSIGN](NANDDRIVERSIGN.md) special pages (erase then rewrite). However, for some reason the block is erased but not rewritten. On the next boot (normal boot or ramdisk boot), `WMR_Init` will not find the [NANDDRIVERSIGN](NANDDRIVERSIGN.md) pages and display the following error :

```
[WMR:ERR] NAND format invalid (mismatch, corrupt, read error or blank NAND device)
[WMR:ERR] boolSignatureFound false  boolProductionFormatVerified true nSig 0x0
******************************************************************************
******************************************************************************
AND: NAND initialisation failed due to format mismatch or uninitialised NAND.
AND: Pleae reboot with reformatting enabled.
******************************************************************************
******************************************************************************
Raw NAND FTL failed initialisation
```

When booting normally, iBoot will display this error on the usb shell and enter recovery mode (iTunes logo). When booting a ramdisk, the same error occurs in the kernel, which then reboots the device after sleeping for 20 seconds.

The security epoch for iOS 4 changed with iOS 4.3.4 release :
  * iOS 4.0 - 4.3.3 : security epoch is 1
  * iOS 4.3-4 - 4.3.5 : security epoch is 2

For instance, if the device runs iOS 4.3.4 and a ramdisk with iOS 4.3.3 kernel is booted (without the kernel patch that prevents the epoch update), the device will be in the bricked state. When using the iOS 5 kernel, "epoch update is now deprecated" so we can boot an iOS 5 kernel on an iOS 4 device without problems. However if the device is already bricked one needs a way to restore the correct [NANDDRIVERSIGN](NANDDRIVERSIGN.md) page for the installed iOS version to be able to boot it again.

# Fix #

The idea for the fix is to patch the `WMR_Init` function to force it to run the part of the NAND reformatting code that writes the [NANDDRIVERSIGN](NANDDRIVERSIGN.md) pages without actually reformatting the NAND (and losing all the data). The kernel\_patcher.py script can create a "NAND recovery" kernel by using an iOS 4 IPSW and the --fixnand command line parameter. **The iOS 4 IPSW used must match the installed version so the correct security epoch is written. The generated kernel is only good for fixing the issue, do not use it for any other purpose.**

```
python python_scripts/kernel_patcher.py --fixnand IOS4_IPSW
./redsn0w_mac_0.9.9b8/redsn0w.app/Contents/MacOS/redsn0w -i IOS4_IPSW -r myramdisk.dmg -k fix_nand_kernelcache.release.n88.patched
```

Once the "[FTL:MSG] Read back Signature OK" message is displayed, manually reboot the device (hold home+power). It should then boot normally.

# Details #

The 3 kernel patches used for the fix were added in revision [r88a8950346cc](http://code.google.com/p/iphone-dataprotection/source/detail?r=88a8950346cca5489cdedd7987e451f8c716cdff)

```
__text:808B2616 DF F8 00 05                 LDR.W           R0, =aAndNandInitial ; "AND: NAND initialisation failed due to "...
__text:808B261A B0 47                       BLX             R6
__text:808B261C DF F8 FC 04                 LDR.W           R0, =aAndPleaseReboo ; "AND: Please reboot with reformatting en"...
__text:808B2620 B0 47                       BLX             R6
__text:808B2622 DF F8 F0 04                 LDR.W           R0, =asc_808CBF38 ; "***************************************"...
__text:808B2626 B0 47                       BLX             R6
__text:808B2628 DF F8 E8 04                 LDR.W           R0, =asc_808CBF38 ; "***************************************"...
__text:808B262C F3 E1                       B               loc_808B2A16
```
The last instruction of this error branch is patched to jump to the code that creates the nSig value :
```
__text:808B266A DF F8 B8 14                 LDR.W           R1, =(_PE_get_security_epoch+1)
__text:808B266E 88 47                       BLX             R1 ; _PE_get_security_epoch
__text:808B2670 DF F8 4C 34                 LDR.W           R3, =NANDDRIVERSIGN_buffer
__text:808B2674 DF F8 B0 24                 LDR.W           R2, =0x43313100
__text:808B2678 10 43                       ORRS            R0, R2         ; add current kernel security epoch to signature
__text:808B267A 18 60                       STR             R0, [R3]
__text:808B267C DF F8 AC 04                 LDR.W           R0, =aFtlMsgVsvflReg ; "[FTL:MSG] VSVFL Register  [OK]\n"
```
Then we jump to the code that sets up the flags field and the version string and writes the NANDDRIVERSIGN block.
```
__text:808B2886 C1 48                       LDR             R0, =aFtlMsgFtlForma ; "[FTL:MSG] FTL Format      [OK]\n"
__text:808B2888 D8 47                       BLX             R11 ; sub_804DDC2C
__text:808B288A 8D 48                       LDR             R0, =NANDDRIVERSIGN_buffer
__text:808B288C 08 99                       LDR             R1, [SP,#0x4C+whitening]
__text:808B288E 06 23                       MOVS            R3, #6
...
Set flags
Copy version string
NANDDRIVERSIGN block is written
...
__text:808B2922 A3 48                       LDR             R0, =aFtlMsgReadBa_0 ; "[FTL:MSG] Read back Signature OK\n"
__text:808B2924 B0 47                       BLX             R6
__text:808B2926 01 24                       MOVS            R4, #1
```

Finally we patch the last instruction to an infinite loop so that we have time to read the messages on screen (in verbose mode).