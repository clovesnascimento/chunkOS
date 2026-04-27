#!/bin/bash

# CHUNK OS Build Script
echo "🔧 CHUNK OS Builder v1.0"

# Cria estrutura de diretórios
mkdir -p build/lib
mkdir -p build/bin
mkdir -p /chunk/etc
mkdir -p /chunk/logs
mkdir -p /chunk/models/registry
mkdir -p /chunk/models/weights

echo "📦 Compilando Kernel..."
cd kernel && make && cp *.so ../build/lib/ && cd ..

echo "📦 Compilando Bibliotecas..."
cd lib && make && cp *.so ../build/lib/ && cd ..

echo "📦 Compilando Drivers..."
cd drivers && make && cp *.so ../build/lib/ && cd ..

echo "📦 Compilando Utilitários..."
cd usr && make && cp chunk-infer chunk-load chunk-monitor chunk-cli.sh ../build/bin/ && cd ..

echo "✅ Build concluído com sucesso!"
echo "Binários em ./build/bin/"
echo "Bibliotecas em ./build/lib/"
