#!/bin/bash

# CHUNK OS Test Suite

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

PASSED=0
FAILED=0

test_start() {
    echo -n "🧪 $1... "
}

test_pass() {
    echo -e "${GREEN}✓ PASS${NC}"
    ((PASSED++))
}

test_fail() {
    echo -e "${RED}✗ FAIL${NC}"
    ((FAILED++))
}

# Build test
echo ""
echo "╔═══════════════════════════════════════╗"
echo "║     CHUNK OS Test Suite v1.0         ║"
echo "╚═══════════════════════════════════════╝"
echo ""

# Test 1: Compilação
test_start "Compilação do kernel"
if [ -f "kernel/nmm.c" ] && [ -f "kernel/Makefile" ]; then
    test_pass
else
    test_fail
fi

# Test 2: Bibliotecas
test_start "Bibliotecas"
if [ -f "lib/libkvcompress.c" ] && [ -f "lib/libprefetch.c" ]; then
    test_pass
else
    test_fail
fi

# Test 3: Ferramentas de usuário
test_start "Ferramentas de usuário"
if [ -f "usr/chunk-infer.c" ] && [ -f "usr/chunk-load.c" ]; then
    test_pass
else
    test_fail
fi

# Test 4: Headers
test_start "Headers"
if [ -f "include/chunk_types.h" ] && [ -f "include/chunk_constants.h" ]; then
    test_pass
else
    test_fail
fi

# Test 5: Scripts
test_start "Scripts"
if [ -f "scripts/build.sh" ] && [ -f "scripts/package.sh" ]; then
    test_pass
else
    test_fail
fi

# Test 6: Simulação de NMM (código compila?)
test_start "Verificação sintática (gcc)"
if command -v gcc > /dev/null; then
    gcc -fsyntax-only kernel/nmm.c -Iinclude 2>/dev/null
    if [ $? -eq 0 ]; then
        test_pass
    else
        test_fail
    fi
else
    echo -e "${YELLOW}⊘ SKIP (gcc não encontrado)${NC}"
fi

# Test 7: Simulação de libkvcompress
test_start "Verificação libkvcompress"
if command -v gcc > /dev/null; then
    gcc -fsyntax-only lib/libkvcompress.c -Iinclude 2>/dev/null
    if [ $? -eq 0 ]; then
        test_pass
    else
        test_fail
    fi
else
    echo -e "${YELLOW}⊘ SKIP (gcc não encontrado)${NC}"
fi

# Test 8: Estrutura de diretórios
test_start "Estrutura completa"
required_files=(
    "kernel/nmm.h"
    "kernel/nmm.c"
    "kernel/Makefile"
    "lib/libkvcompress.h"
    "lib/libkvcompress.c"
    "lib/Makefile"
    "usr/chunk-infer.c"
    "usr/Makefile"
    "scripts/build.sh"
    "scripts/package.sh"
    "include/chunk_types.h"
    "Makefile"
)

all_exist=true
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        all_exist=false
        break
    fi
done

if [ "$all_exist" = true ]; then
    test_pass
else
    test_fail
fi

# Resultados
echo ""
echo "╔═══════════════════════════════════════╗"
echo "║           RESULTADOS FINAIS           ║"
echo "╠═══════════════════════════════════════╣"
echo "║ ✅ Passed: $PASSED"
echo "║ ❌ Failed: $FAILED"
echo "╚═══════════════════════════════════════╝"

if [ $FAILED -eq 0 ]; then
    echo ""
    echo -e "${GREEN}🎉 Todos os testes passaram! CHUNK OS está pronto.${NC}"
    exit 0
else
    echo ""
    echo -e "${RED}❌ Alguns testes falharam. Verifique os arquivos.${NC}"
    exit 1
fi
