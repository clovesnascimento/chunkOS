#!/bin/bash

# CHUNK OS Package Script
# Cria arquivo ROM para instalação

set -e

VERSION="1.0.0"
BUILD_DIR="build"
PACKAGE_NAME="chunk-rom-v${VERSION}"

echo "📦 CHUNK OS Package Builder v${VERSION}"
echo "========================================"

# Cria estrutura
mkdir -p "$BUILD_DIR"/chunk/{bin,lib,etc,models/registry,models/weights,proc,boot}

# Copia binários
echo "📁 Copiando binários..."
cp usr/chunk-infer "$BUILD_DIR"/chunk/bin/ 2>/dev/null || true
cp usr/chunk-load "$BUILD_DIR"/chunk/bin/ 2>/dev/null || true
cp usr/chunk-monitor "$BUILD_DIR"/chunk/bin/ 2>/dev/null || true
cp kernel/*.so "$BUILD_DIR"/chunk/lib/ 2>/dev/null || true
cp lib/*.so "$BUILD_DIR"/chunk/lib/ 2>/dev/null || true

# Cria arquivo de versão
echo "📝 Criando metadata..."
cat > "$BUILD_DIR"/chunk/etc/version << EOF
CHUNK OS v${VERSION}
Build: $(date -I)
Author: Cloves Nascimento
Organization: CNGSM
Signature: CNGSM-CHUNK-$(date +%Y%m%d)
EOF

# Cria modelo dummy para teste
echo "🔧 Criando modelo dummy..."
cat > "$BUILD_DIR"/chunk/models/registry/dummy.meta << EOF
name: dummy
version: 1.0
layers: 4
total_params: 1000000
weight_format: fp16
EOF

# Configuração padrão
cat > "$BUILD_DIR"/chunk/etc/chunk.conf << EOF
# CHUNK OS Configuration
[system]
version = $VERSION
author = "Cloves Nascimento - CNGSM"

[memory]
ram_limit_mb = 1536
eviction_policy = importance

[prefetch]
lookahead = 2
min_confidence = 0.3

[kv_cache]
compression = hybrid
window_size = 1024
sparsity_ratio = 0.1

[dma]
channels = 4
page_size = 262144
EOF

# Script init
cat > "$BUILD_DIR"/chunk/init.sh << 'EOF'
#!/bin/bash
echo "🚀 Iniciando CHUNK OS..."
export LD_LIBRARY_PATH=/chunk/lib:$LD_LIBRARY_PATH
export CHUNK_RAM_LIMIT_MB=1536
echo "✅ CHUNK OS pronto para uso"
echo ""
/chunk/bin/chunk-infer dummy "Bem-vindo ao CHUNK OS"
EOF
chmod +x "$BUILD_DIR"/chunk/init.sh

# Assinatura digital
echo "🔐 Gerando assinatura CNGSM..."
cat > "$BUILD_DIR"/chunk/etc/signature << EOF
CNGSM-CHUNK-${VERSION}-$(date +%Y%m%d-%H%M%S)
Author: Cloves Nascimento
Arquiteto de Ecossistemas Cognitivos
Hash: $(find "$BUILD_DIR"/chunk -type f -exec sha256sum {} \; | sort | sha256sum | cut -d' ' -f1)
EOF

# Cria ZIP
echo "🗜️ Empacotando..."
cd "$BUILD_DIR"
zip -r "../${PACKAGE_NAME}.zip" chunk/ > /dev/null
cd ..

# Calcula checksum
if command -v sha256sum > /dev/null; then
    CHECKSUM=$(sha256sum "${PACKAGE_NAME}.zip" | cut -d' ' -f1)
    echo "$CHECKSUM  ${PACKAGE_NAME}.zip" > "${PACKAGE_NAME}.zip.sha256"
    echo ""
    echo "✅ Pacote criado: ${PACKAGE_NAME}.zip"
    echo "🔐 SHA256: $CHECKSUM"
fi

echo ""
echo "Para instalar:"
echo "  unzip ${PACKAGE_NAME}.zip -d /"
echo "  /chunk/init.sh"
