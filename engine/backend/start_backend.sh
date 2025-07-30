#!/bin/bash

# Obtém o diretório onde o script está localizado
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Ativa o ambiente virtual localizado no mesmo diretório
source "$SCRIPT_DIR/venv/bin/activate"

# Executa o Uvicorn. Agora ele será encontrado porque o venv está ativo.
# O exec substitui o processo do script pelo do uvicorn, o que é mais limpo.
exec uvicorn app.main:app --host localhost --port 8000

