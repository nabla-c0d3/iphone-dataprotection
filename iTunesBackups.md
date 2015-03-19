# iOS 3 #

Password derivation function : PBKDF2 with 2000 iterations.

Each file is encrypted using AES256 in CBC mode, with a unique key and IV. File keys are protected by a master AuthKey stored encrypted by the backup passcode key in the backup Manifest.

The device [Keychain](Keychain.md) SQLite file is backuped, but can only be decrypted with key 0x835 for that device (and thus cannot be restored to another device).

# iOS 4 & 5 #

Starting with iOS 4, a backup keybag is generated for each backup. Class keys in that keybag are different than the ones in the system keybag, and protected by a passcode key derivated from the backup password. The derivation algorithm is PBKDF2 with 10000 iterations (default value for the ITER parameter in the keybag).

Files are encrypted using AES256 in CBC mode, with a unique key and a null IV. File keys are stored wrapped by a class key from the backup keybag (like for HFSContentProtection on the device).

The keychain is backed up as a plist file (keychain-backup.plist), and can be migrated between devices (items with thisDeviceOnly protection classes won't migrate).

The keychain can only migrate if a passcode is set for the backup :
  * if no backup password is set, all keychain class keys (6-11) in the backup keybag are protected by blank passcode key + key 0x835 (WRAP=3) : can only be restored to originating device
  * if a backup password is set, migratable keychain class keys (6-8) are protected by the backup passcode key (WRAP=2). ThisDeviceOnly class keys are protected by backup passcode key + key 0x835 (WRAP=3).

# Tools #

The **backup\_tool.py** script can extract and decrypt iTunes backups.
The **keychain\_tool.py** script handles iOS 4 & 5 backup keychains.

# References #

  * Satish B published a detailed video on iTunes backups forensic analysis: http://www.youtube.com/watch?v=cqj4Z8VkJyU