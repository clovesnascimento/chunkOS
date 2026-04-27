# CHUNK OS Kernel Makefile

CC = gcc
CFLAGS = -Wall -Wextra -O2 -fPIC -I../include
LDFLAGS = -shared -lpthread

KERNEL_OBJS = nmm.o page_fault_handler.o memory_manager.o
KERNEL_LIB = libchunk_kernel.so

all: $(KERNEL_LIB)

$(KERNEL_LIB): $(KERNEL_OBJS)
	$(CC) $(LDFLAGS) -o $@ $^

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f *.o *.so

install:
	cp $(KERNEL_LIB) /chunk/lib/

.PHONY: all clean install
