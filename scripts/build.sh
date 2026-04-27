#!/bin/bash

# CHUNK OS Build Script
# Engenheiros da Próxima Geração

set -e

echo "🔧 CHUNK OS Builder v1.0"
echo "========================="

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Verifica dependências
check_deps() {
    echo -n "Verificando dependências... "
    for dep in gcc make cmake python3; do
        if ! command -v $dep &> /dev/null; then
            echo -e "${RED}FAIL${NC}"
            echo "Erro: $dep não encontrado"
            exit 1
        fi
    done
    echo -e "${GREEN}OK${NC}"
}

# Compila kernel
build_kernel() {
    echo -n "Compilando kernel... "
    cd kernel
    make clean > /dev/null 2>&1
    make > /dev/null 2>&1
    cd ..
    echo -e "${GREEN}OK${NC}"
}

# Compila bibliotecas
build_libs() {
    echo -n "Compilando bibliotecas... "
    cd lib
    make clean > /dev/null 2>&1
    make > /dev/null 2>&1
    cd ..
    echo -e "${GREEN}OK${NC}"
}

# Compila usuário
build_usr() {
    echo -n "Compilando utilitários... "
    cd usr
    make clean > /dev/null 2>&1
    make > /dev/null 2>&1
    cd ..
    echo -e "${GREEN}OK${NC}"
}

# Cria estrutura de diretórios
create_dirs() {
    echo -n "Criando estrutura de diretórios... "
    mkdir -p build/chunk/{bin,lib,etc,models/registry,models/weights,proc}
    echo -e "${GREEN}OK${NC}"
}

# Copia binários
copy_binaries() {
    echo -n "Copiando binários... "
    cp usr/chunk-infer build/chunk/bin/ 2>/dev/null || true
    cp usr/chunk-load build/chunk/bin/ 2>/dev/null || true
    cp usr/chunk-monitor build/chunk/bin/ 2>/dev/null || true
    cp lib/*.so build/chunk/lib/ 2>/dev/null || true
    cp kernel/*.so build/chunk/lib/ 2>/dev/null || true
    echo -e "${GREEN}OK${NC}"
}

# Gera modelo de exemplo
generate_example_model() {
    echo -n "Gerando modelo de exemplo... "
    cat > build/chunk/models/registry/llama-3-8b.meta << EOF
name: llama-3-8b
version: 3.0
format: chunk-v1
layers: 32
total_params: 8000000000
weight_format: fp16
page_size: 262144
kv_cache_pages: 65536
EOF
    echo -e "${GREEN}OK${NC}"
}

# Cria script de inicialização
create_init_script() {
    cat > build/chunk/init.sh << 'EOF'
#!/bin/bash
export LD_LIBRARY_PATH=/chunk/lib:$LD_LIBRARY_PATH
export CHUNK_RAM_LIMIT_MB=1536
echo "CHUNK OS iniciado"
/chunk/bin/chunk-infer llama-3-8b "Bem-vindo ao CHUNK"
EOF
    chmod +x build/chunk/init.sh
}

# Empacota
package() {
    echo -n "Empacotando CHUNK ROM... "
    cd build
    zip -r ../chunk-rom-v1.0.zip chunk/ > /dev/null 2>&1
    cd ..
    echo -e "${GREEN}OK${NC}"
    echo ""
    echo -e "${GREEN}✅ CHUNK OS construído com sucesso!${NC}"
    echo "📦 Arquivo: chunk-rom-v1.0.zip"
    echo ""
    echo "Para instalar:"
    echo "  unzip chunk-rom-v1.0.zip -d /"
    echo "  /chunk/init.sh"
}

# Main
main() {
    check_deps
    create_dirs
    build_kernel
    build_libs
    build_usr
    copy_binaries
    generate_example_model
    create_init_script
    package
}

main "$@"
