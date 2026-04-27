# CHUNK OS Root Makefile

all: build

build:
	chmod +x scripts/*.sh
	./scripts/build.sh

install:
	./scripts/install.sh /chunk

test:
	./scripts/test.sh

clean:
	cd kernel && make clean
	cd lib && make clean
	cd drivers && make clean
	cd usr && make clean
	rm -rf build/

package:
	./scripts/package.sh

.PHONY: all build install test clean package
