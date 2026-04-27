# CHUNK OS Libraries Makefile

CC = gcc
CFLAGS = -Wall -Wextra -O2 -fPIC -I../include
LDFLAGS = -shared

LIB_OBJS = libkvcompress.o libprefetch.o
LIB_OUT = libchunk_utils.so

all: $(LIB_OUT)

$(LIB_OUT): $(LIB_OBJS)
	$(CC) $(LDFLAGS) -o $@ $^

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f *.o *.so

install:
	mkdir -p /chunk/lib/
	cp $(LIB_OUT) /chunk/lib/

.PHONY: all clean install
