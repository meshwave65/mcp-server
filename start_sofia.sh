#!/bin/bash
# Este é o script mestre para iniciar todo o ecossistema SOFIA.

# Garante que o script pare se qualquer comando falhar
set -e

# Navega para o diretório onde o script está (a raiz do projeto)
cd "$(dirname "$0")"

echo "--- [start_sofia.sh] Iniciando o Ecossistema SOFIA ---"
echo "[INFO] Diretório de trabalho atual: $(pwd)"

# --- Carregamento das Variáveis de Ambiente ---
if [ -f ".env" ]; then
    echo "[INFO] Carregando variáveis de ambiente do arquivo .env..."
    # Exporta as variáveis para que fiquem disponíveis para os subprocessos (uvicorn)
    export $(grep -v '^#' .env | xargs)
    echo "[INFO] Variáveis de ambiente carregadas."
else
    echo "[ERRO CRÍTICO] Arquivo de configuração '.env' não encontrado. Não é possível continuar."
    exit 1
fi

# --- Ativação do Ambiente Virtual ---
if [ -d "venv" ]; then
    echo "[INFO] Ativando o ambiente virtual (venv)..."
    source venv/bin/activate
    echo "[INFO] Ambiente virtual ativado. Python executável: $(which python)"
else
    echo "[AVISO] Ambiente virtual 'venv' não encontrado. Tentando executar com o python do sistema."
fi

# --- Execução do Servidor Principal ---
# Executa o Uvicorn apontando para o orquestrador main.py na raiz.
echo "[INFO] Iniciando o servidor Uvicorn para o orquestrador principal..."
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

