# Introduction #

YaFTL is the page-mapping FTL used since iOS 3 (not related to [yaftl](http://code.google.com/p/yaftl/)).


![http://wiki.iphone-dataprotection.googlecode.com/hg/yaftl_translation.svg](http://wiki.iphone-dataprotection.googlecode.com/hg/yaftl_translation.svg)


```
// Page types (as defined in the spare data "type" bitfield)
#define PAGETYPE_INDEX		(0x4)	// Index block indicator
#define PAGETYPE_LBN		(0x10)	// User data 
#define PAGETYPE_FTL_CLEAN	(0x20)	// FTL context (unmounted, clean)
#define PAGETYPE_VFL		(0x80)	// VFL context

...
typedef struct {
    uint32_t lpn;            // Logical page number
    uint32_t usn;            // Update sequence number
    uint8_t  field_8;
    uint8_t  type;            // Page type
    uint16_t field_A;
} __attribute__((packed)) SpareData;
```

# References #

  * https://github.com/iDroid-Project/openiBoot/blob/master/ftl-yaftl/yaftl.c
  * https://github.com/iDroid-Project/openiBoot/blob/master/ftl-yaftl/includes/ftl/yaftl_common.h
  * [DFTL: A Flash Translation Layer Employing Demand-based Selective Caching of Page-level Address Mappings](http://csl.cse.psu.edu/publications/dftl-asplos09.pdf)