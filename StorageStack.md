# iPhone 2G (3.1.3) #

```
+-o flash-controller0@F00000 (AppleARMIODevice)
  +-o AppleS5L8900XADMFMC
    +-o disk@F  (IOFlashStorageDevice)
      +-o AppleNANDFTL
        +-o IOFlashBlockDevice
          +-o IOBlockStorageDriver
            +-o unknown vendor unknown product Media  (IOMedia)
              +-o IOMediaBSDClient
              +-o IOFDiskPartitionScheme
                +-o Untitled 1@1
                | +-o IOMediaBSDClient
                +-o Untitled 2@2
                  +-o IOMediaBSDClient
```

# iPad 1 (4.2.1) #

updated from iOS 3.2 (EncryptedMediaFilter).

```
+-o Root
  | {
  |   "OS Build Version" = "8C148"
  |   "IOKitBuildVersion" = "Darwin Kernel Version 10.4.0: Wed Oct 20 20:14:45 PDT 2010; root:xnu-1504.58.28~3/RELEASE_ARM_S5L8930X"
  +-o K48AP  <class IOPlatformExpertDevice, registered, matched, active, busy 0, retain 23>
    +-o AppleARMPE
    | +-o arm-io@BFC00000 (IOPlatformDevice)
    | | +-o AppleS5L8930XIO
    | |   +-o flash-controller0@1200000  (AppleARMIODevice)
    | |   | +-o AppleS5L8920XIOPFMI
    | |   |   +-o disk@FFFF (IOFlashStorageDevice)
    | |   |     +-o AppleNANDLegacyFTL
    | |   |       +-o IOFlashBlockDevice
    | |   |         +-o IOBlockStorageDriver
    | |   |           +-o unknown vendor unknown product Media  (IOMedia)
    | |   |             +-o IOMediaBSDClient
    | |   |             +-o IOFDiskPartitionScheme
    | |   |               +-o Untitled 1@1  (IOMedia)
    | |   |               | +-o IOMediaBSDClient
    | |   |               +-o Untitled 2@2  (IOMedia)
    | |   |                 +-o IOMediaBSDClient
    | |   |                 +-o EncryptedMediaFilter
    | |   |                   +-o IOMedia@1
    | |   |                     +-o IOMediaBSDClient
```

# iPhone 4 (5.1) #

```
+-o Root
  | {
  |   "OS Build Version" = "9B176"
  |   "IOKitBuildVersion" = "Darwin Kernel Version 11.0.0: Wed Feb  1 23:17:16 PST 2012; root:xnu-1878.11.8~1/RELEASE_ARM_S5L8930X"
  +-o N90AP (IOPlatformExpertDevice)
    +-o AppleARMPE
    | +-o arm-io@BFC00000 (IOPlatformDevice)
    | | +-o AppleS5L8930XIO
    | |   +-o flash-controller0@1200000  (AppleARMIODevice)
    | |   | +-o AppleIOPFMI
    | |   |   +-o disk  (IOFlashStorageDevice)
    | |   |     +-o IOFlashPartitionScheme
    | |   |       +-o IOFlashStoragePartition@4
    | |   |       | +-o AppleNANDLegacyFTL
    | |   |       |   +-o IOFlashBlockDevice
    | |   |       |   | +-o IOBlockStorageDriver
    | |   |       |   |   +-o unknown vendor unknown product Media  (IOMedia)
    | |   |       |   |     +-o IOMediaBSDClient
    | |   |       |   |     +-o LightweightVolumeManager
    | |   |       |   |       +-o IOMedia@1
    | |   |       |   |         +-o IOMediaBSDClient
    | |   |       |   |         +-o IOGUIDPartitionScheme
    | |   |       |   |           +-o System@1  (IOMedia)
    | |   |       |   |           | +-o IOMediaBSDClient
    | |   |       |   |           +-o Data@2  (IOMedia)
    | |   |       |   |             +-o IOMediaBSDClient
```

# iPhone 4S (5.0.1) #

[AppleSwissPPNFTL](AppleSwissPPNFTL.md) replaces [AppleNANDLegacyFTL](AppleNANDLegacyFTL.md).

```
+-o Root
  | {
  |   "OS Build Version" = "9A406"
  |   "IOKitBuildVersion" = "Darwin Kernel Version 11.0.0: Tue Nov  1 20:34:16 PDT 2011; root:xnu-1878.4.46~1/RELEASE_ARM_S5L8940X"
  +-o N94AP (IOPlatformExpertDevice)
    +-o AppleARMPE
    | +-o arm-io@3FB00000 (IOPlatformDevice)
    | | +-o AppleS5L8940XIO
    | |   +-o flash-controller0@1200000  (AppleARMIODevice)
    | |   | +-o AppleIOPFMI
    | |   |   +-o disk  (IOFlashStorageDevice)
    | |   |     +-o IOFlashPartitionScheme
    | |   |       +-o IOFlashStoragePartition@4
    | |   |       | +-o AppleSwissPPNFTL
    | |   |       |   +-o IOFlashBlockDevice
    | |   |       |   | +-o IOBlockStorageDriver
    | |   |       |   |   +-o unknown vendor unknown product Media  (IOMedia)
    | |   |       |   |     +-o IOMediaBSDClient
    | |   |       |   |     +-o LightweightVolumeManager
    | |   |       |   |       +-o IOMedia@1
    | |   |       |   |         +-o IOMediaBSDClient
    | |   |       |   |         +-o IOGUIDPartitionScheme
    | |   |       |   |           +-o System@1  (IOMedia)
    | |   |       |   |           | +-o IOMediaBSDClient
    | |   |       |   |           +-o Data@2  (IOMedia)
    | |   |       |   |             +-o IOMediaBSDClient
```

# iPhone 5 (6.x) #

new drivers: AppleNANDTemperatureSensor, AppleIOFSNANDConfigAccess

```
+-o Root
  | {
  |   "IOKitBuildVersion" = "Darwin Kernel Version 13.0.0: Sun Dec 16 20:01:39 PST 2012; root:xnu-2107.7.55~11/RELEASE_ARM_S5L8950X"
  +-o N41AP  (IOPlatformExpertDevice)
    +-o AppleARMPE
    | +-o arm-io@3FB00000   (IOPlatformDevice)
    | | +-o AppleS5L8950XIO
    | |   +-o flash-controller0@1200000  (AppleARMIODevice)
    | |   | +-o AppleIOPFMI
    | |   |   +-o AppleNANDTemperatureSensor
    | |   |   | +-o IOHIDUserClientIniter
    | |   |   | +-o IOHIDEventServiceUserClient
    | |   |   +-o disk@FFFF  (IOFlashStorageDevice)
    | |   |     +-o IOFlashPartitionScheme
    | |   |       +-o IOFlashStoragePartition@4
    | |   |       | +-o AppleSwissPPNFTL
    | |   |       |   +-o IOFlashBlockDevice
    | |   |       |   | +-o IOBlockStorageDriver
    | |   |       |   |   +-o unknown vendor unknown product Media  (IOMedia)
    | |   |       |   |     +-o IOMediaBSDClient
    | |   |       |   |     +-o LightweightVolumeManager
    | |   |       |   |       +-o IOMedia@1
    | |   |       |   |         +-o IOMediaBSDClient
    | |   |       |   |         +-o IOGUIDPartitionScheme
    | |   |       |   |           +-o System@1  (IOMedia)
    | |   |       |   |           | +-o IOMediaBSDClient
    | |   |       |   |           +-o Data@2    (IOMedia)
    | |   |       |   |             +-o IOMediaBSDClient
    | |   |       |   +-o AppleIOFSNANDConfigAccess
    | |   |       |     +-o AppleDiagnosticDataAccessReadOnly
    | |   |       +-o IOFlashStoragePartition@7
    | |   |       | +-o AppleNANDFactoryBBT
    | |   |       +-o IOFlashStoragePartition@0
    | |   |       +-o IOFlashStoragePartition@1
    | |   |       | +-o AppleEffaceableNAND
    | |   |       +-o IOFlashStoragePartition@2
    | |   |       | +-o IOFlashNVRAM
    | |   |       +-o IOFlashStoragePartition@3
    | |   |       | +-o AppleNANDFirmware
    | |   |       |   +-o AppleImage3NORAccess
    | |   |       |     +-o AppleImage3NORAccessUserClient
    | |   |       +-o IOFlashStoragePartition@5
    | |   |       +-o IOFlashStoragePartition@6
```

# iPhone 5S (7.x) #

[ASPStorage](ASPStorage.md)

```
+-o Root
  | {
  |   "IOKitBuildVersion" = "Darwin Kernel Version 14.0.0: Mon Sep  9 20:56:02 PDT 2013; root:xnu-2423.1.74~2/RELEASE_ARM64_S5L8960X"
  |   "OS Build Version" = "11A470a"
  | 
  +-o N51AP  (IOPlatformExpertDevice)
    +-o AppleARMPE
    | +-o arm-io@2240000 (IOPlatformDevice)
    | | +-o AppleS5L8960XIO
    | |   +-o ans@8040000 (AppleARMIODevice)
    | |   | +-o AppleA7IOP
    | |   |   +-o AppleCSI
    | |   |     +-o management (AppleCSIEndpointService)
    | |   |     +-o console (AppleCSIEndpointService)
    | |   |     +-o crashlog (AppleCSIEndpointService)
    | |   |     +-o syslog (AppleCSIEndpointService)
    | |   |     +-o asp (AppleCSIEndpointService)
    | |   |     | +-o ASPStorage
    | |   |     |   +-o ASPTemperatureSensor
    | |   |     |   | +-o IOHIDUserClientIniter
    | |   |     |   | +-o IOHIDEventServiceUserClient
    | |   |     |   +-o ASPBlockStorage
    | |   |     |   | +-o IONANDBlockDevice
    | |   |     |   |   +-o IOBlockStorageDriver
    | |   |     |   |     +-o Apple NAND Media (IOMedia) disk0
    | |   |     |   |       +-o IOMediaBSDClient
    | |   |     |   |       +-o LightweightVolumeManager
    | |   |     |   |         +-o LwVMMedia@1 (IOMedia) disk0s1
    | |   |     |   |           +-o LwVMMediaBSDClient
    | |   |     |   |           +-o IOGUIDPartitionScheme
    | |   |     |   |             +-o System@1 (IOMedia) disk0s1s1
    | |   |     |   |             | +-o IOMediaBSDClient
    | |   |     |   |             +-o Data@2 (IOMedia) disk0s1s2
    | |   |     |   |               +-o IOMediaBSDClient
    | |   |     |   +-o ASPNVRAM
    | |   |     |   +-o ASPEffaceable
    | |   |     |   | +-o IOEffaceableDevice
    | |   |     |   |   +-o AppleEffaceableBlockDevice
    | |   |     |   |     +-o AppleMobileApNonce
    | |   |     |   +-o ASPDiagnostic
    | |   |     |   | +-o AppleDiagnosticDataAccessReadOnly
    | |   |     |   +-o ASPFirmware
    | |   |     |   | +-o IOFirmwareDevice
    | |   |     |   |   +-o IOBlockStorageDriver
    | |   |     |   |     +-o Apple Firmware Media (IOMedia) disk1
    | |   |     |   |       +-o IOMediaBSDClient 
    | |   |     |   +-o ASPLLBFirmware
    | |   |     |     +-o IOLLBFirmwareDevice
    | |   |     |       +-o IOBlockStorageDriver
    | |   |     |         +-o Apple LLB Media (IOMedia) disk2
    | |   |     |           +-o IOMediaBSDClient
    | |   |     +-o fastsimtest (AppleCSIEndpointService)
    | |   |     +-o iop_kdebug  (AppleCSIEndpointService)
```