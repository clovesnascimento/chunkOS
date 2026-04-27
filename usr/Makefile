# CHUNK OS User Tools Makefile

CC = gcc
CFLAGS = -Wall -Wextra -O2 -I../include
LDFLAGS = -L../kernel -L../lib -L../drivers -lchunk_kernel -lchunk_utils -lchunk_drivers -lpthread

UTILS = chunk-infer chunk-load chunk-monitor

all: $(UTILS)

chunk-infer: chunk-infer.c
	$(CC) $(CFLAGS) -o $@ $< $(LDFLAGS)

chunk-load: chunk-load.c
	$(CC) $(CFLAGS) -o $@ $< $(LDFLAGS)

chunk-monitor: chunk-monitor.c
	$(CC) $(CFLAGS) -o $@ $< $(LDFLAGS)

clean:
	rm -f $(UTILS)

install:
	mkdir -p /chunk/bin/
	cp $(UTILS) /chunk/bin/
	cp chunk-cli.sh /chunk/bin/

.PHONY: all clean install
