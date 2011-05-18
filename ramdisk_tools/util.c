#include <stdio.h>
#include <stdint.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <CoreFoundation/CoreFoundation.h>
#include "util.h"


void printBytesToHex(const uint8_t* buffer, size_t bytes)
{
    while(bytes > 0) {
        printf("%02x", *buffer);
        buffer++;
        bytes--;
    }
}

void printHexString(const char* description, const uint8_t* buffer, size_t bytes)
{
    printf("%s : ", description);
    printBytesToHex(buffer, bytes);
    printf("\n");
}

int write_file(const char* filename, uint8_t* data, size_t len)
{
    int fd = open(filename, O_CREAT | O_RDWR);
    if (fd < 0)
        return -1;
    if (write(fd, data, len) != len)
        return -1;
    close(fd);
    return 0;
}

int getHFSInfos(struct HFSInfos *infos)
{
    char buf[8192] = {0};
    struct HFSPlusVolumeHeader* header;
    int fd = open("/dev/rdisk0s2", O_RDONLY);
    if (fd < 0 )
        return fd;
    lseek(fd, 0, SEEK_SET);
    
    if (read(fd, buf, 8192) != 8192)
        return -1;
    close(fd);
        
    header = (struct HFSPlusVolumeHeader*) &buf[0x400];
    
    uint32_t blockSize = CFSwapInt32BigToHost(header->blockSize);
    
    infos->volumeUUID = header->volumeUUID;
    infos->blockSize = blockSize;
    
    if (blockSize != 0x1000 && blockSize != 0x2000)
    {
        printf("Unknown block size %x\n", blockSize);
    }
    else
    {
        fd = open("/dev/rdisk0", O_RDONLY);
        if (fd < 0 )
            return fd;
        lseek(fd, 2*blockSize, SEEK_SET);
        
        if (read(fd, buf, 8192) != 8192)
            return -1;
        close(fd);
        
        infos->dataVolumeOffset = ((unsigned int*)buf)[0xA0/4];
    }
    return 0;
}

CFMutableStringRef CreateHexaCFString(uint8_t* buffer, size_t len)
{
    int i;
    
    CFMutableStringRef s = CFStringCreateMutable(kCFAllocatorDefault, len*2);
    
    for(i=0; i < len; i++)
    {
        CFStringAppendFormat(s, NULL, CFSTR("%02x"), buffer[i]);
    }
    return s;
}

void addHexaString(CFMutableDictionaryRef out, CFStringRef key, uint8_t* buffer, size_t len)
{
    CFMutableStringRef s = CreateHexaCFString(buffer, len);
    CFDictionaryAddValue(out, key, s);
    CFRelease(s);
}

void saveResults(CFStringRef filename, CFMutableDictionaryRef out)
{
    CFURLRef fileURL = CFURLCreateWithFileSystemPath( NULL, filename, kCFURLPOSIXPathStyle, FALSE);
    CFWriteStreamRef stream = CFWriteStreamCreateWithFile( NULL, fileURL);
    CFWriteStreamOpen(stream);
    CFPropertyListWriteToStream(out, stream, kCFPropertyListXMLFormat_v1_0, NULL);
    CFWriteStreamClose(stream);
    
    CFRelease(stream);
    CFRelease(fileURL);
}