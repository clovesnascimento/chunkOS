#!/bin/bash

# CHUNK OS Test Suite
echo "🧪 Iniciando testes do CHUNK OS..."

export LD_LIBRARY_PATH=./build/lib:$LD_LIBRARY_PATH

# Teste 1: Inicialização do sistema
echo -n "Teste 1: Inicialização do NMM... "
./build/bin/chunk-load dummy > /dev/null 2>&1
if [ $? -eq 0 ]; then echo "✅ PASS"; else echo "❌ FAIL"; exit 1; fi

# Teste 2: Inferência simulada
echo -n "Teste 2: Inferência básica... "
./build/bin/chunk-infer dummy "Teste unitário" > /dev/null 2>&1
if [ $? -eq 0 ]; then echo "✅ PASS"; else echo "❌ FAIL"; exit 1; fi

# Teste 3: Verificação de bibliotecas
echo -n "Teste 3: Integridade das bibliotecas... "
ls build/lib/libchunk_kernel.so build/lib/libchunk_utils.so > /dev/null 2>&1
if [ $? -eq 0 ]; then echo "✅ PASS"; else echo "❌ FAIL"; exit 1; fi

echo "🎉 Todos os testes passaram!"
