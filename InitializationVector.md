# iOS 3/4 #

The IV for AES CBC mode NAND encryption on iOS 3/4 is computed using the following function :

```
void iv_for_lba(uint32_t lpn, uint32_t* iv)
{
    int i;
    for(i = 0; i < 4; i++)
    {
        if(lba & 1)
            lba = 0x80000061 ^ (lba >> 1);
        else
            lba = lba >> 1;
        iv[i] = lba;
    }
}
```

The input parameter is the logical page number of the page being encrypted/decrypted.

# iOS 5+ #

iOS 5 introduced "offset based IV" for [content protected files](HFSContentProtection.md). As stated in the [Apple iOS Security document](http://images.apple.com/iphone/business/docs/iOS_Security_Oct12.pdf) :

  * "The initialization vector (IV) is the output of a linear feedback shift register (LFSR) calculated with the block offset into the file, encrypted with the SHA-1 hash of the per-file key".

The LFSR is the same iv\_for\_lba function. The HFS content protection code implements the offset based IV computation :

```
//xnu-2050.22.13/bsd/sys/cprotect.h
/* 
 * Runtime-only structure containing the content protection status 
 * for the given file.  This is contained within the cnode 
 * This is passed down to IOStorageFamily via the bufattr struct
 *
 ******************************************************
 * Some Key calculation information for offset based IV
 ******************************************************
 * Kf  = original 256 bit per file key
 * Kiv = SHA1(Kf), use full Kf, but truncate Kiv to 128 bits
 * Kiv can be cached in the cprotect, so it only has to be calculated once for the file init
 *
 * IVb = Encrypt(Kiv, offset)
 *
 */
struct cprotect {
    uint32_t    cp_flags;
    uint32_t    cp_pclass;
    aes_encrypt_ctx    cp_cache_iv_ctx;
    uint32_t    cp_cache_key_len;
    uint8_t        cp_cache_key[CP_MAX_KEYSIZE];
    uint32_t    cp_persistent_key_len;
    uint8_t        cp_persistent_key[];
};

//xnu-2050.22.13/bsd/hfs/hfs_cprotect.c
/* Setup AES context */
static int
cp_setup_aes_ctx(struct cprotect *entry)
{
    SHA1_CTX sha1ctxt;
    uint8_t    cp_cache_iv_key[CP_IV_KEYSIZE]; /* Kiv */
    
    /* First init the cp_cache_iv_key[] */
    SHA1Init(&sha1ctxt);
    SHA1Update(&sha1ctxt, &entry->cp_cache_key[0], CP_MAX_KEYSIZE);
    SHA1Final(&cp_cache_iv_key[0], &sha1ctxt);
    
    aes_encrypt_key128(&cp_cache_iv_key[0], &entry->cp_cache_iv_ctx);

    return 0;
}
```

The encrypted file contents can be moved around in the partition, since the IV is only tied to the file key and the file offset, instead of the location on the partition.

```
//xnu-2050.22.13/bsd/hfs/hfs_vfsops.c
/* 
 * Reclaim blocks from regular files.
 *
 * This function iterates over all the record in catalog btree looking 
 * for files with extents that overlap into the space we're trying to 
 * free up.  If a file extent requires relocation, it looks up the vnode 
 * and calls function to relocate the data.
 *
 * Returns:
 *     Zero on success, non-zero on failure. 
 */
static int 
hfs_reclaim_filespace(struct hfsmount *hfsmp, u_int32_t allocLimit, vfs_context_t context) 
{
    //...
#if CONFIG_PROTECT
    int keys_generated = 0;
    /*
     * For content-protected filesystems, we may need to relocate files that
     * are encrypted.  If they use the new-style offset-based IVs, then
     * we can move them regardless of the lock state.  We create a temporary
     * key here that we use to read/write the data, then we discard it at the
     * end of the function.
     */
    if (cp_fs_protected (hfsmp->hfs_mp)) {
        error = cp_entry_gentempkeys(&hfsmp->hfs_resize_cpentry, hfsmp);
        if (error) {
            printf("hfs_reclaimspace: Error generating temporary keys for resize (%d)\n", error);
            goto reclaim_filespace_done;
        }
    }
#endif
```

Offset based IVs are used to decrypt chunks of 4096 bytes (regardless of page size) if the **use-4k-aes-chain** property is set (it is set in device tree in iOS 5).


# References #

  * http://opensource.apple.com/source/xnu/xnu-2050.22.13/bsd/sys/cprotect.h
  * http://opensource.apple.com/source/xnu/xnu-2050.22.13/bsd/hfs/hfs_cprotect.c
  * http://opensource.apple.com/source/xnu/xnu-2050.22.13/bsd/hfs/hfs_vfsops.c

  * [US20130073870 - Secure relocation of encrypted files](https://www.google.com/patents/US20130073870)