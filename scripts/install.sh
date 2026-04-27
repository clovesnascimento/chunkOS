#!/bin/bash

# CHUNK OS Installation Script
INSTALL_ROOT=${1:-/chunk}

echo "🚀 Instalando CHUNK OS em $INSTALL_ROOT..."

mkdir -p $INSTALL_ROOT/bin
mkdir -p $INSTALL_ROOT/lib
mkdir -p $INSTALL_ROOT/etc
mkdir -p $INSTALL_ROOT/models/registry
mkdir -p $INSTALL_ROOT/models/weights
mkdir -p $INSTALL_ROOT/logs

# Copia binários e libs
cp build/bin/* $INSTALL_ROOT/bin/
cp build/lib/* $INSTALL_ROOT/lib/
cp config/chunk.conf $INSTALL_ROOT/etc/
cp config/models.yaml $INSTALL_ROOT/etc/

# Ajusta permissões
chmod +x $INSTALL_ROOT/bin/*

echo "✅ Instalação concluída!"
echo "Adicione ao seu PATH: export PATH=\$PATH:$INSTALL_ROOT/bin"
echo "Adicione ao seu LD_LIBRARY_PATH: export LD_LIBRARY_PATH=\$LD_LIBRARY_PATH:$INSTALL_ROOT/lib"
