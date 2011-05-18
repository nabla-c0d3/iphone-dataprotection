struct HFSInfos {
    uint64_t    volumeUUID;
    uint32_t    blockSize;
    uint32_t    dataVolumeOffset;
};

struct HFSPlusVolumeHeader {
    uint16_t              signature;
    uint16_t              version;
    uint32_t              attributes;
    uint32_t              lastMountedVersion;
    uint32_t              journalInfoBlock;
 
    uint32_t              createDate;
    uint32_t              modifyDate;
    uint32_t              backupDate;
    uint32_t              checkedDate;
 
    uint32_t              fileCount;
    uint32_t              folderCount;
 
    uint32_t              blockSize;
    uint32_t              totalBlocks;
    uint32_t              freeBlocks;
 
    uint32_t              nextAllocation;
    uint32_t              rsrcClumpSize;
    uint32_t              dataClumpSize;
    uint32_t              nextCatalogID;
 
    uint32_t              writeCount;
    uint64_t              encodingsBitmap;
 
    uint32_t              finderInfo[6];
    uint64_t              volumeUUID;
 /*
    HFSPlusForkData     allocationFile;
    HFSPlusForkData     extentsFile;
    HFSPlusForkData     catalogFile;
    HFSPlusForkData     attributesFile;
    HFSPlusForkData     startupFile;*/
} __attribute__((packed));


int getHFSInfos(struct HFSInfos *infos);

CFMutableStringRef CreateHexaCFString(uint8_t* buffer, size_t len);

void printBytesToHex(const uint8_t* buffer, size_t bytes);
void printHexString(const char* description, const uint8_t* buffer, size_t bytes);
int write_file(const char* filename, uint8_t* data, size_t len);

void addHexaString(CFMutableDictionaryRef out, CFStringRef key, uint8_t* buffer, size_t len);
void saveResults(CFStringRef filename, CFMutableDictionaryRef out);

