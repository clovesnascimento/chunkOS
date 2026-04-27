#!/bin/bash

# CHUNK OS CLI Helper
CHUNK_BIN="/chunk/bin"
CHUNK_LIB="/chunk/lib"

export LD_LIBRARY_PATH=$CHUNK_LIB:$LD_LIBRARY_PATH

show_help() {
    echo "CHUNK OS CLI v1.0.0"
    echo "Uso: chunk-cli <comando> [argumentos]"
    echo ""
    echo "Comandos:"
    echo "  load <modelo>      Carrega um modelo"
    echo "  infer <mod> <pr>   Executa inferência"
    echo "  monitor            Abre o monitor do sistema"
    echo "  list               Lista modelos registrados"
    echo "  status             Mostra status do kernel"
    echo "  help               Mostra esta ajuda"
}

case "$1" in
    load)
        $CHUNK_BIN/chunk-load "${@:2}"
        ;;
    infer)
        $CHUNK_BIN/chunk-infer "${@:2}"
        ;;
    monitor)
        $CHUNK_BIN/chunk-monitor
        ;;
    list)
        ls /chunk/models/registry/*.meta
        ;;
    status)
        echo "CHUNK Kernel: Online"
        echo "NMM Context: Active"
        ;;
    *)
        show_help
        ;;
esac
