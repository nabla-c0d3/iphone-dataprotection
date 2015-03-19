# Description #

Special pages are stored in the last blocks of a CE. On devices that support encryption, these pages are encrypted using the [Metadata Key](EncryptionKeys.md).

# Header Format #

```
char name[0x34]; //null padded name 
uint32_t length;
uint8_t data[0x38 - length];
```

# Types #

Only in CE 0 :
  * [NANDDRIVERSIGN](NANDDRIVERSIGN.md)
  * [DEVICEUNIQUEINFO](DEVICEUNIQUEINFO.md)
  * [DIAGCONTROLINFO](DIAGCONTROLINFO.md)

In all CEs :
  * [DEVICEINFOBBT](DEVICEINFOBBT.md)