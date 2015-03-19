# iOS 3 and below #

| 16-byte IV | AES128(key835, IV, data + SHA1(data)) |
|:-----------|:--------------------------------------|

# iOS 4 #

| version (0) | protection\_class | AESWRAP(class\_key, item\_key) (40 bytes) | AES256(item\_key, data) |
|:------------|:------------------|:------------------------------------------|:------------------------|

# iOS 5 #

| version (2) | protection\_class | len\_wrapped\_key | AESWRAP(class\_key, item\_key) (len\_wrapped\_key) | AES256\_GCM(item\_key, data) | integrity\_tag (16 bytes) |
|:------------|:------------------|:------------------|:---------------------------------------------------|:-----------------------------|:--------------------------|