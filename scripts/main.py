# sofia/main.py (Versão Simplificada)
import os
import sys
from fastapi import FastAPI
from dotenv import load_dotenv
from pathlib import Path

# --- Configuração de Caminho ---
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))
load_dotenv(dotenv_path=PROJECT_ROOT / '.env')

# --- Importações dos Roteadores ---
from backend.app.routes import roadmap_router, segments_router, tasks_router
from fsmw_module.app.routes import fsmw_router

# --- Criação da Aplicação FastAPI ---
app = FastAPI(title="Ecossistema SOFIA Unificado", version="5.2.0")
print("--- ℹ️  Inicializando a aplicação SOFIA (Arquitetura Modular Autônoma)... ---")

# --- REGISTRO DE TODAS AS ROTAS ---
app.include_router(roadmap_router.router, tags=["SOFIA - Roadmap"])
app.include_router(segments_router.router, tags=["SOFIA - Segments"])
app.include_router(tasks_router.router, tags=["SOFIA - Tasks"])
print("--- ✅ Módulos de rotas do SOFIA registrados. ---")

app.include_router(fsmw_router.router, prefix="/fsmw", tags=["FSMW - File System Module"])
print("--- ✅ Módulo de rotas do FSMW registrado. ---")

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Bem-vindo ao Ecossistema SOFIA v5.2 (Unificado)"}

