#!/bin/bash
# Ponto de entrada DEDICADO para o microsserviço Backend SOFIA.

# Garante que o script pare se qualquer comando falhar
set -e

# --- INÍCIO DA CORREÇÃO CRÍTICA ---
# Navega para a RAIZ DO PROJETO ('sofia/'), um nível ACIMA de onde o script está.
# Isso é essencial para que o Python e o Uvicorn entendam a importação 'backend.main'.
cd "$(dirname "$0")/.."
echo "--- [start_backend.sh] Iniciando o Backend SOFIA ---"
echo "[INFO] Diretório de trabalho alterado para a raiz do projeto: $(pwd)"
# --- FIM DA CORREÇÃO CRÍTICA ---

# --- Ativação do Ambiente Virtual ---
# O venv está no diretório de trabalho atual (a raiz do projeto)
if [ -d "venv" ]; then
    echo "[INFO] Ativando o ambiente virtual da raiz do projeto..."
    source venv/bin/activate
else
    echo "[ERRO CRÍTICO] Ambiente virtual 'venv' não encontrado na raiz."
    exit 1
fi

# --- Carregamento das Variáveis de Ambiente ---
# O .env também está no diretório de trabalho atual
if [ -f ".env" ]; then
    echo "[INFO] Exportando variáveis de ambiente do arquivo .env da raiz..."
    export $(grep -v '^#' .env | xargs)
else
    echo "[AVISO] Arquivo '.env' não encontrado na raiz."
fi

# --- Execução do Servidor ---
echo "[INFO] Iniciando o servidor Uvicorn para o Backend SOFIA..."
# Agora, o comando aponta para 'backend.main:app', que o Uvicorn
# encontrará porque estamos na raiz do projeto.
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload

