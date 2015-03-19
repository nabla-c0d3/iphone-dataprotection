# Description #

iOS kernel extension that manages keybags.

Keybag types :
  * System
  * Backup
  * Escrow
  * OTA (iOS 5)

# IOKit interface #

Accessible through the MobileKeyBag private framework functions.

| Selector | Description | Comment |
|:---------|:------------|:--------|
| 0  | initUserClient |  |
| 1  | ? |  |
| 2  | AppleKeyStoreKeyBagCreate |  |
| 3  | AppleKeyStoreKeyBagCopyData |  |
| 4  | AppleKeyStoreKeyBagRelease  |  |
| 5  | AppleKeyStoreKeyBagSetSystem |  |
| 6  | AppleKeyStoreKeyBagCreateWithData |  |
| 7  | AppleKeyStoreKeyBagGetLockState |  |
| 8  | AppleKeyStoreLockDevice |  |
| 9  | AppleKeyStoreUnlockDevice |  |
| 10 | AppleKeyStoreKeyWrap |  |
| 11 | AppleKeyStoreKeyUnwrap |  |
| 12 | AppleKeyStoreKeyBagUnlock |  |
| 13 | AppleKeyStoreKeyBagLock |  |
| 14 | AppleKeyStoreKeyBagGetSystem |  |
| 15 | AppleKeyStoreKeyBagChangeSecret |  |
| 16 | ? |  |
| 17 | AppleKeyStoreGetDeviceLockState |  |
| 18 | AppleKeyStoreRecoverWithEscrowBag |  |
| 19 | AppleKeyStoreOblitClassD | erases the [DKey](EncryptionKeys.md), used during wipe ([Obliteration](Obliteration.md))   |
| 20 | AppleKeyStoreDrainBackupKeys | collect rewrapped file keys for iCloud backup (see F\_TRANSCODEKEY fcntl) |
| 21 | AppleKeyStoreSetBakup1? |  |
| 22 | AppleKeyStoreSetBakup2? |  |