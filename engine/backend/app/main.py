# sofia/engine/backend/app/main.py (VERSÃO FINAL CORRIGIDA)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# --- CORREÇÃO (1/2) ---
# Importamos 'Base' e 'engine' diretamente do arquivo 'database',
# que é a fonte da verdade para a configuração do banco de dados.
from .database import engine, Base 
from . import models
from .routers import roadmap_router

# --- CORREÇÃO (2/2) ---
# Agora usamos o 'Base' que importamos diretamente.
# Esta linha garante que as tabelas SQLAlchemy (definidas em models.py
# e que herdam de Base) sejam criadas no banco de dados se não existirem.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SOFIA Backend API",
    description="API para o sistema SOFIA e seus projetos gerenciados.",
    version="1.0.0"
)

# Configuração do CORS para permitir requisições de qualquer origem
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui as rotas definidas no arquivo roadmap_router.py
app.include_router(roadmap_router.router)

@app.get("/", tags=["Root"])
def read_root():
    """
    Rota raiz para verificar rapidamente se a API está online e operacional.
    """
    return {"message": "Bem-vindo à API do SOFIA. O serviço está operacional."}

