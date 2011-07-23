/**
  * GreenPois0n Cynanide - patch.c
  * Copyright (C) 2010 Chronic-Dev Team
  * Copyright (C) 2010 Joshua Hill
  *
  * This program is free software: you can redistribute it and/or modify
  * it under the terms of the GNU General Public License as published by
  * the Free Software Foundation, either version 3 of the License, or
  * (at your option) any later version.
  *
  * This program is distributed in the hope that it will be useful,
  * but WITHOUT ANY WARRANTY; without even the implied warranty of
  * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  * GNU General Public License for more details.
  *
  * You should have received a copy of the GNU General Public License
  * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 **/

#include <stdio.h>
#include <string.h>

#include "patch.h"
#include "device.h"
#include "commands.h"

typedef struct kpatch{
	char* description;
	char* search;
	char* replace;
	int length;
	int found;
} kpatch;

kpatch patchs[]= {
	{"CSED", "\x00\x00\x00\x00\x01\x00\x00\x00\x80\x00\x00\x00\x00\x00\x00\x00", "\x01\x00\x00\x00\x01\x00\x00\x00\x80\x00\x00\x00\x00\x00\x00\x00", 16,0},
	{"AMFI", "\x01\xD1\x01\x30\x04\xE0\x02\xDB", "\x00\x20\x01\x30\x04\xE0\x02\xDB", 8,0},
	{"UID", "\x56\xD0\x40\xF6", "\x00\x00\x40\xF6", 4,0},
	{"NAND_epoch", "\x90\x47\x83\x45", "\x90\x47\x00\x20",4,0},
};
#define NPATCHS 	sizeof(patchs)/sizeof(kpatch)

int patch_kernel(unsigned char* kaddr, unsigned int size) {
	unsigned int j;
	unsigned char* end = kaddr + size;
	
	while(kaddr < end)
	{
		for(j = 0; j < NPATCHS; j++)
		{
			if (patchs[j].found)
				continue;
			
			if(!memcmp(patchs[j].search, kaddr, patchs[j].length))
			{
				memcpy(kaddr, patchs[j].replace, patchs[j].length);
				patchs[j].found = 1;
			}
		}
		kaddr++;
	}
	return 0;
}


unsigned char* patch_find(unsigned char* start, int length, unsigned char* find, int size) {
	int i = 0;
	for(i = 0; i < length; i++) {
		if(!memcmp(&start[i], find, size)) {
			return &start[i];
		}
	}
	return NULL;
}

unsigned char* patch_rfind(unsigned char* start, int length, unsigned char* find, int size) {
	int i = 0;
	for(i = length; i < length; i--) {
		if(!memcmp(&start[i], find, size)) {
			return &start[i];
		}
	}
	return NULL;
}
