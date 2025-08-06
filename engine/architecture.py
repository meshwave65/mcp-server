# ~/home/sofia/engine/architecture.py
# Define caminhos e variáveis essenciais para o ecossistema SOFIA.

from pathlib import Path
import sys
import os

# --- Raiz do projeto (engine) ---
ENGINE_ROOT = Path(__file__).resolve().parent

# --- Diretórios ---
FRONTEND_DIR = ENGINE_ROOT / "frontend"
BACKEND_DIR = ENGINE_ROOT / "backend"

# --- Caminho do Python dentro do venv ---
VENV_PYTHON = Path(os.getenv("VENV_PYTHON", sys.executable))

# --- Arquivo .env ---
ENV_FILE = ENGINE_ROOT.parent / ".env"

# --- Portas ---
BACKEND_PORT = int(os.getenv("BACKEND_PORT", 8000))
FRONTEND_PORT = int(os.getenv("FRONTEND_PORT", 5173))

