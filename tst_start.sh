#!/bin/bash
# Ponto de entrada DEDICADO e ISOLADO para o microsserviço FSMW.

# Garante que o script pare se qualquer comando falhar
set -e

# Navega para a RAIZ DO PROJETO ('sofia/'), dois níveis ACIMA de onde o script está.
# Isso é essencial para que o Python e o Uvicorn entendam a importação 'fsmw_module.main'.
cd "$(dirname "$0")/.."
echo "--- [fsmw_module/start.sh] Iniciando o Módulo FSMW em modo isolado ---"
echo "[INFO] Diretório de trabalho alterado para a raiz do projeto: $(pwd)"

# Ativa o ambiente virtual que está na raiz do projeto
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "[ERRO] venv não encontrado na raiz." && exit 1
fi

# Carrega as variáveis do .env que está na raiz
if [ -f ".env" ]; then
    export $(grep -v '^#' .env | xargs)
else
    echo "[ERRO] .env não encontrado na raiz." && exit 1
fi

echo "[INFO] Iniciando o servidor Uvicorn para FSMW na porta 8001..."
# Executa o Uvicorn apontando para o main.py do FSMW.
# Como estamos na raiz, o caminho do módulo é 'fsmw_module.main'.
PYTHONPATH=. uvicorn fsmw_module.main:app --host 0.0.0.0 --port 8001 --reload

