#!/bin/bash
# Ponto de entrada DEDICADO para o Ecossistema Unificado.

set -e

# Navega para a RAIZ DO ENGINE, um nível ACIMA de onde o script está.
cd "$(dirname "$0")/.."
echo "--- [start_backend.sh] Iniciando o Ecossistema Unificado ---"
echo "[INFO] Diretório de trabalho alterado para a raiz do engine: $(pwd)"

# Ativa o ambiente virtual que está um nível acima do engine
if [ -d "../venv" ]; then
    source ../venv/bin/activate
else
    echo "[ERRO CRÍTICO] Ambiente virtual 'venv' não encontrado na raiz do projeto."
    exit 1
fi

# Exporta as variáveis de ambiente da raiz do projeto
if [ -f "../.env" ]; then
    export $(grep -v '^#' ../.env | xargs)
else
    echo "[AVISO] Arquivo '.env' não encontrado na raiz do projeto."
fi

# Executa o Uvicorn com o contexto correto
echo "[INFO] Iniciando o servidor Uvicorn para o Ecossistema Unificado..."
# Como estamos no 'engine', o Python encontrará o pacote 'backend'
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload

