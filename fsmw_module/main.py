# ~/home/sofia/fsmw_module/main.py
# VERSÃO FINAL: Corrige o caminho para a pasta 'static' DENTRO de 'app'.

import sys
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# --- Configuração de Caminho ---
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# --- Importação do Roteador do FSMW ---
from fsmw_module.app.routes import fsmw_router

# --- Criação da Aplicação FastAPI ---
app = FastAPI(
    title="FSMW - Módulo de Gerenciamento de Arquivos",
    version="1.4.0" # Versão final e funcional
)

# --- INÍCIO DA CORREÇÃO CRÍTICA ---
# Monta o diretório 'static' que está DENTRO da pasta 'app'.
# O caminho agora aponta para 'fsmw_module/app/static/'.
static_path = Path(__file__).resolve().parent / "app" / "static"
app.mount("/static", StaticFiles(directory=static_path), name="static")
# --- FIM DA CORREÇÃO CRÍTICA ---

# Habilita o CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui as rotas do FSMW na aplicação
app.include_router(fsmw_router.router)

@app.get("/")
def read_root_fsmw():
    """Rota raiz para verificar se o módulo FSMW está online."""
    return {"message": "Bem-vindo ao Módulo FSMW."}

