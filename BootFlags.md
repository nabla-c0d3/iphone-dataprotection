# nand-disable-driver #

This flag disables the FTL driver (and not the "NAND driver"), thus preventing the creation of the disk0 block device. The [IOFlashControllerUserClient](IOFlashControllerUserClient.md) interface can still be used to access the NAND, so this flag is useful to setup a forensically sound NAND acquisition environement.

Because of redsn0w's 40 characters boot-args limit, the kernel\_patcher.py script remplaces the "nand-disable-driver" string with "nand-disable" in the kernel binary.

# nand-readonly #

iOS 5 kernel boot argument that prevents write access to the NAND. Logical partitions cannot be mounted at all, since the LwVM layer is blocked :

```
LwVM::start - failed to open base media read/write
```

However, in the case of an unclean shutdown, the kernel crashes after the FTL restore operation.

# nand-enable-adm #

nand-enable-adm=0 prevents the AppleIOPFMI service from starting. Not very useful.