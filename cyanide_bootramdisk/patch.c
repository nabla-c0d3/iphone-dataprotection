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


int patch_kernel(unsigned char* address, unsigned int size) {
	unsigned int target = 0;
	/*
	CSED: 00 00 00 00 01 00 00 00 80 00 00 00 00 00 00 00 => 01 00 00 00 01 00 00 00 80 00 00 00 00 00 00 00 ; armv6 & armv7

	AMFI: 00 B1 00 24 20 46 90 BD  +  0 => 00 B1 01 24 20 46 90 BD ; armv7
	      0E 00 A0 E1 01 10 84 E2  + 20 => 00 00 00 00 ; armv6

	TFP0: 85 68 00 23 02 93 01 93  +  8 => 0B E0 C0 46 ; armv7
	      85 68 .. 93 .. 93 00 2c          0B D1
	      85 68 02 93 01 93 00 2C  +  8 => 0E 93 BD 93 ; armv6
	*/
	unsigned int i = 0;
	for(i = 0; i < size; i++) {
        if(!memcmp(&address[i], "\x56\xD0\x40\xF6", 4)) {
			target = i;
			memcpy(&address[target], "\x00\x00\x40\xF6", 4);
			continue;
		}
		//4.3.1 AMFI
		if(!memcmp(&address[i], "\x01\xD1\x01\x30\x04\xE0\x02\xDB", 8)) {
			target = i + 0;
			memcpy((char*) &address[target], "\x00\x20\x01\x30\x04\xE0\x02\xDB", 8);
			continue;
		}
		/*
		 * Patch 1
		 */
		if(!memcmp(&address[i], "\x00\x00\x00\x00\x01\x00\x00\x00\x80\x00\x00\x00\x00\x00\x00\x00", 16)) {
			target = i + 0;
			memcpy(&address[target], "\x01\x00\x00\x00\x01\x00\x00\x00\x80\x00\x00\x00\x00\x00\x00\x00", 16);
			continue;
		}

		/*
		 * Patch 2
		 */
		if(!memcmp(&address[i], "\x00\xB1\x00\x24\x20\x46\x90\xBD", 8)) {
			target = i + 0;
			memcpy((char*) &address[target], "\x00\xB1\x01\x24\x20\x46\x90\xBD", 8);
			continue;
		}
		if(!memcmp(&address[i], "\x00\x00\x50\xE3\x00\x00\x00\x0A\x00\x40\xA0\xE3\x04\x00\xA0\xE1", 16)) {
			target = i + 8;
			memcpy((char*) &address[target], "\x01\x40\xA0\xE3", 4);
			continue;
		}

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
