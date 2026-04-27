# CHUNK OS User Tools Makefile

CC = gcc
CFLAGS = -Wall -Wextra -O2 -I../include -I../kernel -I../lib
LDFLAGS = -L../kernel -L../lib -lchunk_kernel -lkvcompress -lprefetch -lpthread -lm

TOOLS = chunk-infer chunk-load chunk-monitor

all: $(TOOLS)

chunk-infer: chunk-infer.o
	$(CC) -o $@ $^ $(LDFLAGS)

chunk-load: chunk-load.o
	$(CC) -o $@ $^ $(LDFLAGS)

chunk-monitor: chunk-monitor.o
	$(CC) -o $@ $^ $(LDFLAGS)

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f *.o $(TOOLS)

install:
	cp $(TOOLS) /chunk/bin/

.PHONY: all clean install
