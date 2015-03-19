# iOS 4 #

| **Key id (CLAS)** | **Protection class** | **Comment** |
|:------------------|:---------------------|:------------|
| 1 | NSProtectionComplete |  |
| 2 | (NSFileProtectionWriteOnly) | undocumented, behaves like NSProtectionComplete |
| 3 | (NSFileProtectionCompleteUntilUserAuthentication) | undocumented, behaves like NSProtectionComplete |
| 4 | NSProtectionNone | stored in EffaceableArea |
| 5 | unknown ? (NSFileProtectionRecovery ?) |  undocumented |
| 6 | kSecAttrAccessibleWhenUnlocked |  |
| 7 | kSecAttrAccessibleAfterFirstUnlock |  |
| 8 | kSecAttrAccessibleAlways |  |
| 9 | kSecAttrAccessibleWhenUnlockedThisDeviceOnly |  |
| 10 | kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly |  |
| 11 | kSecAttrAccessibleAlwaysThisDeviceOnly |  |

# iOS 5 #

| **Key id (CLAS)** | **Protection class** | **Comment** |
|:------------------|:---------------------|:------------|
| 1 | NSProtectionComplete |  |
| 2 | NSFileProtectionCompleteUnlessOpen  | uses ECDH over D. J. Bernstein's [Curve25519](http://cr.yp.to/ecdh/curve25519-20060209.pdf) |
| 3 | NSFileProtectionCompleteUntilFirstUserAuthentication  | like AfterFirstUnlock but for files  |
| 4 | NSProtectionNone | stored in EffaceableArea |
| 5 | unknown ? (NSFileProtectionRecovery ?) |  undocumented |
| 6 | kSecAttrAccessibleWhenUnlocked |  |
| 7 | kSecAttrAccessibleAfterFirstUnlock |  |
| 8 | kSecAttrAccessibleAlways |  |
| 9 | kSecAttrAccessibleWhenUnlockedThisDeviceOnly |  |
| 10 | kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly |  |
| 11 | kSecAttrAccessibleAlwaysThisDeviceOnly |  |