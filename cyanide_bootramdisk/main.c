/**
  * GreenPois0n Cynanide - main.c
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
#include <stdlib.h>
#include <string.h>

#include "patch.h"
#include "commands.h"
#include "device.h"

unsigned int find_string(unsigned char* data, unsigned int base, unsigned int size, const char* name) {
	// First find the string
	int i = 0;
	unsigned int address = 0;
	for(i = 0; i < size; i++) {
		if(!memcmp(&data[i], name, strlen(name))) {
			address = &data[i];
			break;
		}
	}
	return address;
}

void* find_kernel_bootargs() {
	return find_string(IBSS_BASEADDR, IBSS_BASEADDR, 0x40000, "rd=md0");
}

int main() {
	int i = 0;
	char* gBootArgs = find_kernel_bootargs();
	if (gBootArgs != NULL)
	{
        strcpy(gBootArgs, "rd=md0 -v");
	}
    cmd_rdboot();
	return 0;
}

