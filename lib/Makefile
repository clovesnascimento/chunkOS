# CHUNK OS Libraries Makefile

CC = gcc
CFLAGS = -Wall -Wextra -O2 -fPIC -I../include -I.
LDFLAGS = -shared -lm

LIBS = libkvcompress.so libprefetch.so

all: $(LIBS)

libkvcompress.so: libkvcompress.o
	$(CC) $(LDFLAGS) -o $@ $^

libprefetch.so: libprefetch.o
	$(CC) $(LDFLAGS) -o $@ $^

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f *.o *.so

install:
	cp *.so /chunk/lib/

.PHONY: all clean install
