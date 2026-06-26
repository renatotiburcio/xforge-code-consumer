#!/bin/bash
#
# xforge install (Linux/macOS)
# Instala xforge CLI no PATH do usuario.
#
# Uso:
#   bash install.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLI_PATH="$SCRIPT_DIR/cli.py"

if [ ! -f "$CLI_PATH" ]; then
    echo "[XForge] ERRO: cli.py nao encontrado em $SCRIPT_DIR"
    exit 1
fi

# Criar wrapper
BIN_DIR="${HOME}/.local/bin"
mkdir -p "$BIN_DIR"

WRAPPER_PATH="$BIN_DIR/xforge"
cat > "$WRAPPER_PATH" << EOF
#!/bin/bash
exec python3 "$CLI_PATH" "\$@"
EOF
chmod +x "$WRAPPER_PATH"

echo "[XForge] Instalado em: $WRAPPER_PATH"

# Adicionar ao PATH se necessario
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    SHELL_RC=""
    if [ -n "$BASH_VERSION" ]; then
        SHELL_RC="$HOME/.bashrc"
    elif [ -n "$ZSH_VERSION" ]; then
        SHELL_RC="$HOME/.zshrc"
    fi

    if [ -n "$SHELL_RC" ]; then
        echo "" >> "$SHELL_RC"
        echo "# XForge CLI" >> "$SHELL_RC"
        echo "export PATH=\"\$PATH:$BIN_DIR\"" >> "$SHELL_RC"
        echo "[XForge] PATH atualizado em $SHELL_RC (reinicie o terminal)"
    fi
fi

echo ""
echo "[XForge] Testando instalacao..."
python3 "$CLI_PATH" --version

echo ""
echo "[XForge] Pronto! Use 'xforge --help' para comecar."
echo "[XForge] Para usar em qualquer projeto:"
echo "  cd meu-projeto"
echo "  xforge init --analyze"
echo "  xforge recognize"
echo "  xforge doctor"
