# Description #

Apple NAND debugging tool included in restore/upgrade ramdisks. Uses the [IOFlashControllerUserClient](IOFlashControllerUserClient.md) interface to interact with the NAND driver.

```
$ /usr/local/bin/ioflashstoragetool -h
ioflashstoragetool: invalid option -- h
ioflashstoragetool: Low-level NAND flash utility

Options:                                                                      
  --verbose           Be talkative about what the tool is doing.              
  --noisy             Be extremely noisy while doing things.                  
  --quiet             Don't show progress output.                             
  --ignoreBBT         Ignore the factory BBT.                                 
                                                                              
Multi-bank addressing:                                                        
  p<page>             Addresses all banks, starting at bank 0, page <page>.   
  b<block>            Addresses all banks, starting at bank 0, block <block>. 
    In these modes, page/block counts are per-bank and all operations start   
    at bank zero.  <page>/<block> may be decimal or hex preceeded by 0x.      
                                                                              
Single-bank addressing:                                                       
  <bank>p<page>       Addresses bank <bank>, starting at page <page>.         
  <bank>b<block>      Addresses bank <bank>, starting at block <block>.       
    In these modes, page/block counts are for the selected bank only.         
    <bank> is decimal, <page>/<block> may be decimal or hex preceeded by 0x.  
                                                                              
Commands:                                                                     
  read <page address> [<page count>|all] [-|<filename>|<ipaddr>:<port>]              
    Reads pages from NAND.  If <filename> is specified, page data optionally  
    followed by page metadata is written to the file, otherwise the data is   
    formatted for perusal. '-' may be supplied as a filename to cause page    
    data to be written to standard output unformatted.                        
    <page count> defaults if not specified; one page if an explicit bank/page 
    address is specified, one row of pages (bank count) if only a page address
    is specified.                                                             
      --spareAuto           Attempt to automatically determine the spare area 
                            format on a page-by-page basis (default).         
      --spareMeta           Assume all pages have AND metadata.               
      --spareMaxECC         Assume all pages are formatted for maximum ECC and
                            have no metadata.                                 
      --spareRaw            Read the spare area raw, do not perform any ECC.  
      --softErrors          Do not abort on uncorrectable ECC errors.  Perusal
                            output will indicate an uncorrectable page, whilst
                            file output will be replaced with zero bytes.     
      --spareFormatOnly     Print the format determined by spareAuto          
                            but suppress the hexdump.  Only relevant in       
                            perusal mode.                                     
      --noBlankCheck        Disable blank page checking.                      
    XXX note that the <ipaddr>:<port> output specifier is not implemented.    

  write <page address> [<page count>] [-|<filename>|<ipaddr>:<port>]                  
    Writes <page count> pages to the NAND from <filename> or standard input if
    not specified.                                                            
    If <page count> is not supplied, it is inferred from the file size or EOF.
    If the file size is not appropriate, a diagnostic will be printed.  In the
    case where standard input is not aligned, some pages may be written.      
      --spareMeta           Write pages with AND metadata (12 bytes).         
      --spareMaxECC         Write pages with no metadata and maximum ECC.     
      --spareRaw            Write the spare area raw, do not generat any ECC. 
      --softErrors          Do not abort on write errors.                     
    XXX note that the <ipaddr>:<port> input specifier is not implemented.     

  erase <block address> [<block count>|all]                                           
    Erases <block count> blocks within the NAND, starting at <block address>  
    <block count> defaults if not specified; one block if an explicit         
    bank/block is specified, one row of blocks (bank count) if only a block   
    address is specified.                                                     
      --softErrors          Do not abort on erase failures.                   

  unformat     Erases all data on the NAND and removes the AND BBT, returning the device 
    as closely as possible to the original vendor factory format.             
      --addFailedBlocks     Add blocks that fail erasure to the factory-marked
                            bad block list.                                   

  scan     Performs a non-destructive read scan of the NAND and displays statistics  
    on the number of bit errors corrected, bad pages, etc.                    

  scrub [<iterations>]                                                                
    Performs <iterations> erase/write/read scrubs of the writable areas of the
    NAND. Cannot overwrite secure portions of the device, or factory bad      
    blocks.                                                                   

  bbtinfo     Report the contents of the factory bad-block table.                       

  format <partition table type>                                                        
    Writes partition table to pages 0 and 1 of block 0 of all devices.        
    The <partition table type> may be one of: s5l8720x s5l8920x               
      --force               Performs format even if an AND signature is       
                            detected.                                         

  nvram [info|dump]                                                                   
    Examine the physical structure of the nvram partition on boot-from-nand   
    products in order to perform one of the following tasks:                  
      info     Provide summary info about the nvram partition.                
      dump     Output xml tree containing raw content of all readable         
               bootloader format pages in the nvram partition.                

  fwupdate <firmware file>                                                               
    Update the firmware on the attached PPN device                            
      firmware file    File containing firmware for the attached device       
```

A NAND dump can be acquired on iOS 4 using the following command (piped into a listening netcat for instance) :
```
/usr/local/bin/ioflashstoragetool --spareMeta --softErrors --noBlankCheck --quiet read p0 all
```

When using the iOS 4 kernel, ioflashstoragetool can be used directly but be aware that it will cause a kernel panic when reading bootloader blocks (first 16 blocks of each CE) that are present on NAND-only devices (only the nvram command uses the kIOFlashStorageOptionBootPageIO flag).