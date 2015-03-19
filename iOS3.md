# Keychain data column iOS <= 3.x #

| 16-byte IV | AES128(key835, IV, data + SHA1(data)) |
|:-----------|:--------------------------------------|

# iOS 3.x data partition encryption #

See EncryptedMediaFilter