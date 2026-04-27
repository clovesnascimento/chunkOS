# CHUNK OS Drivers Makefile

CC = gcc
CFLAGS = -Wall -Wextra -O2 -fPIC -I../include
LDFLAGS = -shared -lpthread

DRIVER_OBJS = npu_virtual_memory.o flash_dma.o
DRIVER_LIB = libchunk_drivers.so

all: $(DRIVER_LIB)

$(DRIVER_LIB): $(DRIVER_OBJS)
	$(CC) $(LDFLAGS) -o $@ $^

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f *.o *.so

install:
	mkdir -p /chunk/lib/
	cp $(DRIVER_LIB) /chunk/lib/

.PHONY: all clean install
