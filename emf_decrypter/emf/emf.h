//As of iOS 4, class keys 1 to 4 are used for files, class 5 usage is unknown
#define MAX_CLASS_KEYS	5
#define CLASS_DKEY		4

typedef struct EMFInfo
{
	Volume* volume;
	uint64_t volume_id;
	uint64_t volume_offset;
	uint32_t classKeys_bitset;
	AES_KEY emfkey;
	AES_KEY classKeys[MAX_CLASS_KEYS];
}EMFInfo;

EMFInfo* EMF_init(Volume*, char*);

#define CPROTECT_V2_LENGTH		0x38	//56

typedef struct cprotect_xattr_v2
{
	uint16_t version; // =2
	uint16_t zero; // =0
	uint32_t unknown; // leaks stack dword in one code path :)
	uint32_t protection_class_id;
	uint32_t wrapped_length; //0x28
	uint8_t wrapped_key[0x28];
} cprotect_xattr_v2;

#define CPROTECT_V4_LENGTH		0x4C	//76

typedef struct cprotect_xattr_v4
{
	uint16_t version; // =4
	uint16_t zero; // =0
	uint32_t xxx_length; // 0xc
	uint32_t protection_class_id;
	uint32_t wrapped_length; //0x28
	uint8_t xxx_junk[20]; //uninitialized ?
	uint8_t wrapped_key[0x28];
} cprotect_xattr_v4;