#include <stdio.h>
#include <stdint.h>
#include <CoreFoundation/CoreFoundation.h>
#include "device_info.h"
#include "util.h"

int main(int argc, char* argv[])
{
    CFMutableDictionaryRef out = device_info(-1, NULL);
    
    CFShow(out);
   
    CFStringRef plistFileName = CFStringCreateWithFormat(kCFAllocatorDefault, NULL, CFSTR("%@.plist"), CFDictionaryGetValue(out, CFSTR("dataVolumeUUID")));
    saveResults(plistFileName, out);
    CFRelease(out);
    CFRelease(plistFileName);
    return 0;
}
