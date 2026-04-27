#!/bin/bash

# CHUNK OS Install Script
# Instala o sistema no dispositivo

set -e

ROOT="${1:-/}"

echo "🔧 CHUNK OS Installer"
echo "====================="
echo "Destino: $ROOT"
echo ""

# Verifica se é root (para instalação real)
if [ "$ROOT" = "/" ] && [ "$EUID" -ne 0 ]; then
    echo "⚠️ Para instalação no sistema real, execute como root"
    echo "   Use: sudo $0"
    exit 1
fi

# Cria diretórios
echo "📁 Criando diretórios..."
mkdir -p "$ROOT/chunk"/{bin,lib,etc,models/registry,models/weights,proc,boot,logs}

# Copia arquivos
echo "📋 Copiando arquivos..."
if [ -d "build/chunk" ]; then
    cp -r build/chunk/* "$ROOT/chunk/"
else
    echo "❌ Build não encontrado. Execute ./scripts/build.sh primeiro"
    exit 1
fi

# Configura permissões
echo "🔒 Configurando permissões..."
chmod 755 "$ROOT/chunk/bin"/* 2>/dev/null || true
chmod 644 "$ROOT/chunk/lib"/*.so 2>/dev/null || true
chmod 755 "$ROOT/chunk/init.sh"

# Configura PATH (opcional)
if [ -d "$ROOT/etc/profile.d" ]; then
    echo "#!/bin/bash" > "$ROOT/etc/profile.d/chunk.sh"
    echo "export PATH=\$PATH:/chunk/bin" >> "$ROOT/etc/profile.d/chunk.sh"
    echo "export LD_LIBRARY_PATH=\$LD_LIBRARY_PATH:/chunk/lib" >> "$ROOT/etc/profile.d/chunk.sh"
    chmod 644 "$ROOT/etc/profile.d/chunk.sh"
fi

# Configura serviço systemd (se existir)
if [ -d "$ROOT/etc/systemd/system" ]; then
    cat > "$ROOT/etc/systemd/system/chunk.service" << EOF
[Unit]
Description=CHUNK OS Neural Memory Manager
After=network.target

[Service]
Type=simple
ExecStart=/chunk/init.sh
Restart=on-failure
User=root

[Install]
WantedBy=multi-user.target
EOF
    echo "✅ Serviço systemd configurado"
fi

echo ""
echo "✅ CHUNK OS instalado com sucesso em $ROOT"
echo ""
echo "Para iniciar:"
echo "  /chunk/init.sh"
echo ""
echo "Para iniciar automaticamente:"
echo "  systemctl enable chunk"
echo "  systemctl start chunk"
