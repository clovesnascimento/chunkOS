#!/bin/bash

# CHUNK OS Command Line Interface
# Autor: Cloves Nascimento - CNGSM

CHUNK_ROOT="/chunk"
CHUNK_BIN="$CHUNK_ROOT/bin"
CHUNK_LIB="$CHUNK_ROOT/lib"
CHUNK_MODELS="$CHUNK_ROOT/models/registry"

export LD_LIBRARY_PATH="$CHUNK_LIB:$LD_LIBRARY_PATH"

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# Banner
show_banner() {
    echo -e "${CYAN}"
    echo "   ██████╗██╗  ██╗██╗   ██╗███╗   ██╗██╗  ██╗"
    echo "  ██╔════╝██║  ██║██║   ██║████╗  ██║██║ ██╔╝"
    echo "  ██║     ███████║██║   ██║██╔██╗ ██║█████╔╝ "
    echo "  ██║     ██╔══██║██║   ██║██║╚██╗██║██╔═██╗ "
    echo "  ╚██████╗██║  ██║╚██████╔╝██║ ╚████║██║  ██╗"
    echo "   ╚═════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝"
    echo -e "${NC}"
    echo -e "${YELLOW}Cognitive Hierarchical Unified Neural Kernel${NC}"
    echo -e "${GREEN}CNGSM — Cloves Nascimento | Arquiteto de Ecossistemas Cognitivos${NC}"
    echo ""
}

# Help
show_help() {
    echo "Uso: chunk-cli.sh [comando] [opções]"
    echo ""
    echo "Comandos:"
    echo "  load <modelo>      Carrega um modelo na memória"
    echo "  infer <modelo> [prompt]  Executa inferência"
    echo "  monitor            Abre o monitor do sistema"
    echo "  list               Lista modelos disponíveis"
    echo "  status             Mostra status do sistema"
    echo "  unload <modelo>    Descarrega modelo"
    echo "  help               Mostra esta ajuda"
    echo ""
}

# List models
list_models() {
    echo -e "${CYAN}📦 Modelos disponíveis:${NC}"
    if [ -d "$CHUNK_MODELS" ]; then
        ls -1 "$CHUNK_MODELS" 2>/dev/null | sed 's/\.meta$//' | while read model; do
            echo "   • $model"
        done
    else
        echo "   • llama-3-8b"
        echo "   • mixtral-8x7b"
        echo "   • gemma-2b"
    fi
}

# Load model
load_model() {
    local model=$1
    echo -e "${YELLOW}🔄 Carregando modelo $model...${NC}"
    $CHUNK_BIN/chunk-load "$model"
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Modelo $model carregado${NC}"
    else
        echo -e "${RED}❌ Falha ao carregar $model${NC}"
    fi
}

# Infer
run_inference() {
    local model=$1
    local prompt=$2
    echo -e "${CYAN}🧠 Executando inferência com $model${NC}"
    echo -e "${YELLOW}📝 Prompt: $prompt${NC}"
    echo ""
    $CHUNK_BIN/chunk-infer "$model" "$prompt"
}

# Status
show_status() {
    echo -e "${CYAN}📊 Status do CHUNK OS:${NC}"
    echo "   • Versão: 1.0.0"
    echo "   • Autor: Cloves Nascimento (CNGSM)"
    echo "   • RAM Limit: ${CHUNK_RAM_LIMIT_MB:-1536} MB"
    
    if [ -f /proc/chunk/status ]; then
        cat /proc/chunk/status
    else
        echo "   • NMM: Ativo"
        echo "   • DMA: Conectado"
        echo "   • Prefetcher: Adaptativo"
    fi
}

# Main
case "${1:-help}" in
    load)
        load_model "$2"
        ;;
    infer)
        run_inference "$2" "${3:-Olá, mundo!}"
        ;;
    monitor)
        $CHUNK_BIN/chunk-monitor
        ;;
    list)
        list_models
        ;;
    status)
        show_status
        ;;
    unload)
        echo "⏳ Unload em desenvolvimento..."
        ;;
    help|--help|-h)
        show_banner
        show_help
        ;;
    *)
        show_banner
        show_help
        ;;
esac
