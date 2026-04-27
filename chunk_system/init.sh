#!/bin/bash
# CHUNK OS Init Script
# CNGSM — Cloves Nascimento

echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║                                                                  ║"
echo "║   🧠 CHUNK OS — Cognitive Hierarchical Unified Neural Kernel    ║"
echo "║                                                                  ║"
echo "║   📛 CNGSM — Cloves Nascimento                                   ║"
echo "║   🔐 Assinatura: CNGSM-CHUNK-2026-04-26-V1.0                    ║"
echo "║                                                                  ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""

export CHUNK_ROOT=/chunk
export CHUNK_RAM_LIMIT_MB=1536
export LD_LIBRARY_PATH=$CHUNK_ROOT/lib:$LD_LIBRARY_PATH
export PATH=$CHUNK_ROOT/bin:$PATH

echo "✅ CHUNK OS inicializado com sucesso!"
echo ""
echo "Comandos disponíveis:"
echo "  chunk-infer <modelo> <prompt>  - Executa inferência"
echo "  chunk-load <modelo>            - Carrega modelo"
echo "  chunk-monitor                  - Monitora sistema"
echo ""

# Se tiver modelo dummy, testa
if [ -f "$CHUNK_ROOT/bin/chunk-infer" ]; then
    $CHUNK_ROOT/bin/chunk-infer dummy "CHUNK OS operacional!" 2>/dev/null || true
fi
