# sofia/backend/main.py (Versão FastAPI - Correta)
import os
import sys
from fastapi import FastAPI
from dotenv import load_dotenv
from pathlib import Path

# --- Configuração de Caminho ---
# Adiciona a raiz do projeto ('sofia') ao path do Python
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Carrega o .env da raiz do projeto
load_dotenv(dotenv_path=PROJECT_ROOT / '.env')

# --- Importações dos Roteadores FastAPI ---
# Importa os objetos 'router' de cada um dos seus arquivos de rota
from backend.app.routes import roadmap_router, segments_router, tasks_router

# --- Criação da Aplicação FastAPI ---
app = FastAPI(
    title="Ecossistema SOFIA",
    description="API Central para o projeto SOFIA, incluindo o módulo FSMW.",
    version="2.0.0"
)

print("--- ℹ️  Inicializando a aplicação SOFIA (FastAPI)... ---")

# --- REGISTRO DAS ROTAS (ROTEADORES) ---
# Inclui os roteadores na aplicação principal
app.include_router(roadmap_router.router)
app.include_router(segments_router.router)
app.include_router(tasks_router.router)
print("--- ✅ Módulos de rotas do SOFIA registrados. ---")


# --- Rota Principal ---
@app.get("/")
def read_root():
    return {"message": "Bem-vindo ao Ecossistema SOFIA v2.0"}

# --- Ponto de Entrada para Execução com Uvicorn ---
# Para executar, você não usará mais 'python3 -m backend.main'.
# O padrão para FastAPI é usar um servidor ASGI como o Uvicorn.
# O comando será: uvicorn backend.main:app --reload

print("--- ✅ Aplicação SOFIA pronta. Para iniciar, use: uvicorn backend.main:app --reload ---")

