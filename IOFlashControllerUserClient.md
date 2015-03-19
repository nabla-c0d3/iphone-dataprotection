# Description #

The IOFlashControlerUserClient class allows access to the NAND driver from userland.

The kIOFlashControllerReadPage selector can be used to read NAND pages + spare area. On iOS 3 it is possible to read the full spare area (metadata+ECC), this does not seem to be possible starting with iOS 4, only the (12) metadata bytes are read.

All selectors were removed in iOS 5, except kIOFlashControllerDisableKeepout and kIOFlashControllerUpdateFirmware.

| Selector | Description | Comment |
|:---------|:------------|:--------|
| 1  | kIOFlashControllerReadPage |  |
| 2  | kIOFlashControllerWritePage |  |
| 3  | kIOFlashControllerEraseBlock |  |
| 10  | kIOFlashControllerDisableKeepout | requires "SecureRoot" |
| 11  | kIOFlashControllerUpdateFirmware | for PPN devices |

(selectors named after the FSD