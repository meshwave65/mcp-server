# engine/architecture.py
# VERSÃO: 2.2 - Caminhos Absolutos Explícitos

import os
from pathlib import Path
from dotenv import load_dotenv

# Define a raiz do projeto de forma explícita e correta
PROJECT_ROOT = Path("/home/mesh/home/sofia")
load_dotenv(dotenv_path=PROJECT_ROOT / ".env")

# --- Caminhos Fundamentais ---
ENGINE_ROOT = PROJECT_ROOT / "engine"
FRONTEND_DIR = ENGINE_ROOT / "frontend"

# --- Configurações de Rede ---
BACKEND_PORT = 8000
FRONTEND_PORT = 5173

# --- CORREÇÃO CRÍTICA ---
# Define o caminho para o executável Python do venv de forma absoluta e inequívoca.
VENV_PYTHON = "/home/mesh/home/sofia/venv/bin/python"

# --- URL do Banco de Dados ---
SOFIA_DB_URL = os.getenv("SOFIA_DATABASE_URL")
FSMW_DB_URL = os.getenv("FSMW_DATABASE_URL")
