# Tangling KDF #

As stated in the [Apple iOS Security document](http://images.apple.com/iphone/business/docs/iOS_Security_Oct12.pdf) :

"The process by which a user's passcode is turned into a cryptographic key and
strengthened with the device's UID. This ensures that a brute-force attack must be
performed on a given device, and thus is rate limited and cannot be performed in
parallel. The tangling algorithm is PBKDF2, which uses AES as the pseudorandom
function (PRF) with a UID-derived key."

# References #

  * https://code.google.com/p/iphone-dataprotection/source/browse/ramdisk_tools/AppleKeyStore_kdf.c
  * [US20110252243 - System and method for content protection based on a combination of a user pin and a device specific identifier](http://www.google.com/patents/US20110252243)
  * http://blog.crackpassword.com/2012/06/new-hardware-key-for-ipad-3-passcode-verification-or-is-it-just-masking/