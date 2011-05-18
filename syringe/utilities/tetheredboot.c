#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <getopt.h>
#include <sys/stat.h>
#include <stdbool.h>

#include "libpois0n.h"


bool file_exists(const char* fileName)
{
   struct stat buf;
   return !stat(fileName, &buf);
}

void print_progress(double progress, void* data) {
	int i = 0;
	if(progress < 0) {
		return;
	}

	if(progress > 100) {
		progress = 100;
	}

	printf("\r[");
	for(i = 0; i < 50; i++) {
		if(i < progress / 2) {
			printf("=");
		} else {
			printf(" ");
		}
	}

	printf("] %3.1f%%", progress);
	if(progress == 100) {
		printf("\n");
	}
}

void usage()
{
	printf("Usage: tetheredboot -i <ibss> -k <kernelcache> [-r <ramdisk>] [-b <bgcolor>] [-l <bootlogo.img3>]\n");
	exit(0);
}



bool g_verbose = false;

int main(int argc, char* argv[]) {
	int result = 0;
	irecv_error_t ir_error = IRECV_E_SUCCESS;

	//int index;
	const char 
		*ramdiskFile = NULL,
		*payloadFile = NULL;
	int c;

	opterr = 0;

	while ((c = getopt (argc, argv, "vhi:r:p:")) != -1)
		switch (c)
	{
		case 'v':
			g_verbose = true;
			break;
		case 'h':
			usage();
			break;
		case 'r':
			if (!file_exists(optarg)) {
				error("Cannot open ramdisk file '%s'\n", optarg);
				return -1;
			}
			ramdiskFile = optarg;
			break;
		case 'p':
			if (!file_exists(optarg)) {
				error("Cannot open payload file '%s'\n", optarg);
				return -1;
			}
			payloadFile = optarg;
			break;
		default:
			usage();
	}

	if (ramdiskFile == NULL || payloadFile == NULL)
	{
		error("Missing ramdisk or payload file");
		return -1;
	}

	pois0n_init();
	pois0n_set_callback(&print_progress, NULL);

	info("Waiting for device to enter DFU mode\n");
	while(pois0n_is_ready()) {
		sleep(1);
	}

	info("Found device in DFU mode\n");
	result = pois0n_is_compatible();
	if (result < 0) {
		error("Your device in incompatible with this exploit!\n");
		return result;
	}

	result = pois0n_injectonly();
	if (result < 0) {
		error("DFU Exploit injection failed (%u)\n", result);
		return result;
	}
	if (ramdiskFile != NULL)
	{
		boot_ramdisk(payloadFile, ramdiskFile);
	}
	pois0n_exit();
	return 0;
}
