#!/bin/bash
# Ponto de entrada DEDICADO para a Interface Vite.

set -e
cd "$(dirname "$0")"
echo "--- [start_frontend.sh] Iniciando a Interface (Vite) ---"

# Verifica se as dependências estão instaladas (a pasta node_modules)
if [ ! -d "node_modules" ]; then
    echo "[AVISO] Pasta 'node_modules' não encontrada. Executando 'npm install'..."
    npm install
fi

# O comando 'npm run dev' automaticamente usa o vite local do node_modules.
echo "[INFO] Executando 'npm run dev' para iniciar o servidor Vite..."
npm run dev -- --host

