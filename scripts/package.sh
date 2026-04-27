#!/bin/bash

# CHUNK OS Packaging Script
VERSION="1.0.0"
PACKAGE_NAME="chunk-os-v$VERSION.tar.gz"

echo "📦 Empacotando CHUNK OS v$VERSION..."

tar -czf $PACKAGE_NAME \
    kernel/ lib/ drivers/ usr/ include/ \
    scripts/ config/ tools/ docs/ boot/ \
    Makefile README.md LICENSE.cngsm

echo "✅ Pacote criado: $PACKAGE_NAME"
