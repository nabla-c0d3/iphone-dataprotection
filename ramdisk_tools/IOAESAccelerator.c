/**
https://github.com/planetbeing/xpwn/blob/master/crypto/aes.c
**/
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <IOKit/IOKitLib.h>
#include <pthread.h>
#include "IOAESAccelerator.h"
#include "IOKit.h"

io_connect_t conn = 0;
IOByteCount IOAESStructSize = sizeof(IOAESStruct);
pthread_once_t once_control = PTHREAD_ONCE_INIT;


void aes_init()
{
    conn = IOKit_getConnect("IOAESAccelerator");
}

io_connect_t IOAESAccelerator_getIOconnect()
{
    pthread_once(&once_control, aes_init);
    return conn;
}


int doAES(void* inbuf, void *outbuf, uint32_t size, uint32_t keyMask, void* key, void* iv, int mode, int bits) {
    IOReturn ret;
    IOAESStruct in;

    pthread_once(&once_control, aes_init);

    in.mode = mode;
    in.bits = bits;
    in.inbuf = inbuf;
    in.outbuf = outbuf;
    in.size = size;
    in.mask = keyMask;

    memset(in.keybuf, 0, sizeof(in.keybuf));

    if(key)
        memcpy(in.keybuf, key, in.bits / 8);

    if(iv)
        memcpy(in.iv, iv, 16);
    else
        memset(in.iv, 0, 16);

    ret = IOConnectCallStructMethod(conn, kIOAESAcceleratorTask, &in, IOAESStructSize, &in, &IOAESStructSize);
    if(ret == 0xe00002c2) {
        IOAESStructSize = IOAESStruct_sizeold;
        ret = IOConnectCallStructMethod(conn, kIOAESAcceleratorTask, &in, IOAESStructSize, &in, &IOAESStructSize);
    }
            
    if(iv)
        memcpy(iv, in.iv, 16);

    return ret;
}

IOReturn doAES_wrapper(void* thisxxx, int mode, void* iv, void* outbuf, void *inbuf, uint32_t size, uint32_t keyMask)
{
    int x = doAES(inbuf, outbuf, size, keyMask, NULL, iv, mode, 128);
    return !x;
}

int AES_UID_Encrypt(void* input2, void* output, size_t len)
{
    IOAESStruct in;
    IOReturn ret;
    unsigned char* input = malloc(16);
    
    memcpy(input, input2, 16);

    pthread_once(&once_control, aes_init);

    in.mode = kIOAESAcceleratorEncrypt;
    in.mask = kIOAESAcceleratorUIDMask;
    in.bits = 128;
    in.inbuf = input;
    in.outbuf = output;
    in.size = len;
    
    memset(in.keybuf, 0, sizeof(in.keybuf));
    memset(in.iv, 0, 16);

    ret = IOConnectCallStructMethod(conn, kIOAESAcceleratorTask, &in, IOAESStructSize, &in, &IOAESStructSize);
    if(ret == 0xe00002c2) {
        IOAESStructSize = IOAESStruct_sizeold;
        ret = IOConnectCallStructMethod(conn, kIOAESAcceleratorTask, &in, IOAESStructSize, &in, &IOAESStructSize);
    }

    if(ret != kIOReturnSuccess) {
        fprintf(stderr, "IOAESAccelerator returned: %x\n", ret);

    }
    return ret;
}

uint8_t* IOAES_key835()
{
    static uint8_t key835[16] = {0};
    AES_UID_Encrypt("\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01", key835, 16);
    return key835;
}

uint8_t* IOAES_key89B()
{
    static uint8_t key89B[16] = {0};
    AES_UID_Encrypt("\x18\x3E\x99\x67\x6B\xB0\x3C\x54\x6F\xA4\x68\xF5\x1C\x0C\xBD\x49", key89B, 16);
    return key89B;
}