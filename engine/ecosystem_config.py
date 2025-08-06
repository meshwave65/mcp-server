# ~/home/sofia/engine/config.py
# Ponto Único de Verdade para a configuração da arquitetura.

from pathlib import Path

# --- Raiz Operacional ---
# A raiz do engine é o diretório onde este arquivo de config está.
ENGINE_ROOT = Path(__file__).resolve().parent

# --- Raiz do Projeto ---
# A raiz do projeto (onde estão .env e venv) é o diretório pai do engine.
PROJECT_ROOT = ENGINE_ROOT.parent

# --- Caminhos dos Componentes ---
# Caminhos absolutos e inequívocos para cada componente.
BACKEND_DIR = ENGINE_ROOT / 'backend'
FRONTEND_DIR = ENGINE_ROOT / 'frontend'
FSMW_DIR = ENGINE_ROOT / 'fsmw_module'

# --- Caminhos do Ambiente ---
VENV_PYTHON = PROJECT_ROOT / 'venv' / 'bin' / 'python'
ENV_FILE = PROJECT_ROOT / '.env'

# --- Portas dos Serviços ---
# Se precisarmos mudar uma porta, mudamos apenas aqui.
BACKEND_PORT = 8000
FRONTEND_PORT = 5173

