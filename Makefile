# CHUNK OS Master Makefile

.PHONY: all clean kernel lib usr package install test

all: kernel lib usr package

kernel:
	$(MAKE) -C kernel

lib:
	$(MAKE) -C lib

usr:
	$(MAKE) -C usr

package:
	./scripts/package.sh

install:
	./scripts/install.sh

test:
	./scripts/test.sh

clean:
	$(MAKE) -C kernel clean
	$(MAKE) -C lib clean
	$(MAKE) -C usr clean
	rm -rf build/ chunk-rom-*.zip

help:
	@echo "CHUNK OS - Commands:"
	@echo "  make all      - Build everything"
	@echo "  make kernel   - Build only kernel"
	@echo "  make lib      - Build libraries"
	@echo "  make usr      - Build user tools"
	@echo "  make package  - Create ROM zip"
	@echo "  make install  - Install system"
	@echo "  make test     - Run tests"
	@echo "  make clean    - Clean build artifacts"
