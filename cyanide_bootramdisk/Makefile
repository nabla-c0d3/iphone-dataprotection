CROSS ?= arm-elf-
CC = $(CROSS)gcc
LD = $(CROSS)ld
SRC = .
LOADADDR = 0x42F00000
OBJCOPY = $(CROSS)objcopy
OBJECTS = entry.o main.o  commands.o patch.o 
CFLAGS = -I./$(SRC)/include -nostdlib -mlittle-endian
LDFLAGS = -Ttext $(LOADADDR) -nostdlib -lc -lm -lgcc

%.o: $(SRC)/%.S
	$(CC) -c $(<) -o $(@) $(INCLUDES) $(CFLAGS) 

%.o: $(SRC)/%.c
	$(CC) -c $(<) -o $(@) $(INCLUDES) $(CFLAGS) 

all: payload

payload: payload.elf
	xxd -i payload > payload.h
	
payload.elf: $(OBJECTS)
	$(CC) -o $(@) $(OBJECTS) $(LDFLAGS)
	$(OBJCOPY) -O binary $(@) payload

clean:
	rm -rf *.o *.elf payload
	
