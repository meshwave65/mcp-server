# sofia/engine/backend/app/main.py (VERSÃO ATUALIZADA)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from . import models

# --- IMPORTAÇÃO DOS ROTEADORES ---
from .routers import roadmap_router
from .routers import tasks_router  # <-- 1. NOVA LINHA: Importa o roteador de tarefas

# Garante que as tabelas do banco de dados (se houver) sejam criadas.
# models.Base.metadata.create_all(bind=engine) # Descomente se precisar criar tabelas do DB

app = FastAPI(
    title="SOFIA Backend API",
    description="API para o sistema SOFIA e seus projetos gerenciados.",
    version="2.0.0" # Atualizamos a versão para refletir o novo módulo
)

# Habilita o CORS para permitir requisições do frontend
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- REGISTRO DOS ROTEADORES ---
app.include_router(roadmap_router.router)
app.include_router(tasks_router.router) # <-- 2. NOVA LINHA: Inclui o roteador de tarefas

@app.get("/", tags=["Root"])
def read_root():
    """ Rota raiz para verificar se a API está online. """
    return {"message": "Bem-vindo à API do SOFIA. O serviço está operacional."}


