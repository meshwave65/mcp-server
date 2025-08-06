# ~/home/sofia/engine/backend/main.py
# VERSÃO ATUALIZADA: Agora atua como um Gateway de API, unificando backend e fsmw.

import sys
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# --- Configuração de Caminho ---
ENGINE_ROOT = Path(__file__).resolve().parent.parent
if str(ENGINE_ROOT) not in sys.path:
    sys.path.insert(0, str(ENGINE_ROOT))

# --- Importações dos Roteadores de AMBOS os serviços ---
from backend.app.routers import roadmap_router, tasks_router
from fsmw_module.app.routes import fsmw_router  # <-- Importação do FSMW
from backend.app.database import Base, engine

# --- Criação das Tabelas (se não existirem) ---
Base.metadata.create_all(bind=engine)

# --- Criação da Aplicação FastAPI Unificada ---
app = FastAPI(
    title="Ecossistema SOFIA Unificado",
    description="API Central servindo Backend SOFIA e Módulo FSMW.",
    version="1.5.0"
)

# --- Montagem do Diretório Estático do FSMW ---
static_path = ENGINE_ROOT / "fsmw_module" / "app" / "static"
app.mount("/static", StaticFiles(directory=static_path), name="static")

# Habilita o CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- REGISTRO DE TODAS AS ROTAS ---
print("--- Registrando roteadores ---")
app.include_router(roadmap_router.router)
app.include_router(tasks_router.router)
print("✅ Roteadores do Backend SOFIA registrados.")

app.include_router(fsmw_router.router)
print("✅ Roteador do FSMW registrado.")


@app.get("/")
def read_root():
    return {"message": "Bem-vindo ao Ecossistema SOFIA Unificado"}

