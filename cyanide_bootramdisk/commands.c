/**
  * GreenPois0n Cynanide - commands.c
  * Copyright (C) 2010 Chronic-Dev Team
  * Copyright (C) 2010 Joshua Hill
  * Copyright (C) 2010 Cyril Cattiaux
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
#include <stdlib.h>
#include <string.h>

#include "patch.h"
#include "commands.h"
#include "device.h"

int(*jump_to)(int flags, void* addr, int phymem) = NULL;

void hooked(int flags, void* addr, int phymem);

void* find_jump_to() {
	void* bytes = NULL;
	if(strstr((char*) (IBSS_BASEADDR + 0x200), "n72ap")) {
		bytes = patch_find(IBSS_BASEADDR, 0x40000, "\xf0\xb5\x03\xaf\x04\x1c\x15\x1c", 8);
		bytes++;
	} else {
		bytes = patch_find(IBSS_BASEADDR, 0x40000, "\x80\xb5\x00\xaf\x04\x46\x15\x46", 8);
		bytes++;
	}
	return bytes;
}

int cmd_rdboot() {
	int i = 0;
	void* address = NULL;
	void(*hooker)(int flags, void* addr, void* phymem) = &hooked;

	// search for jump_to function
	if(strstr((char*) (IBSS_BASEADDR + 0x200), "n72ap")) {
		jump_to = patch_find(IBSS_BASEADDR, 0x30000, "\xf0\xb5\x03\xaf\x04\x1c\x15\x1c", 8);
	} else {
		// 80  B5  00  AF  04  46  15  46
		jump_to = patch_find(IBSS_BASEADDR, 0x30000, "\x80\xb5\x00\xaf\x04\x46\x15\x46", 8);
	}

    if (jump_to != NULL)
    {
        memcpy(jump_to, "\x00\x4b\x98\x47", 4);
        memcpy(jump_to+4, &hooker, 4);
    }
	return 0;
}

void clear_icache() {
    __asm__("mov r0, #0");
    __asm__("mcr p15, 0, r0, c7, c5, 0");
    __asm__("mcr p15, 0, r0, c7, c5, 4");
    __asm__("nop");
    __asm__("nop");
    __asm__("nop");
    __asm__("nop");
};

void hooked(int flags, void* addr, int phymem) {
	// patch kernel
	patch_kernel((void*)(LOADADDR - 0x1000000), 0xA00000);

	if(strstr((char*) (IBSS_BASEADDR + 0x200), "n72ap")) {
		memcpy(jump_to, "\xf0\xb5\x03\xaf\x04\x1c\x15\x1c", 8);
	} else {
		memcpy(jump_to, "\x80\xb5\x00\xaf\x04\x46\x15\x46", 8);
	}
	clear_icache();

	jump_to++;
	jump_to(flags, addr, phymem);
}
