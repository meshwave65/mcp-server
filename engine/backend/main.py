# engine/backend/main.py
# VERSÃO: 3.2 - Implementando a Importação Explícita do DB

import sys
from pathlib import Path
from fastapi import FastAPI

# Adiciona a raiz do 'engine' ao path para garantir as importações
ENGINE_ROOT = Path(__file__).resolve().parent.parent
if str(ENGINE_ROOT) not in sys.path:
    sys.path.insert(0, str(ENGINE_ROOT))

# --- DIRETRIZ IMPLEMENTADA ---
# Declaração explícita de que 'Base' e 'engine' vêm do módulo 'connect_db'
# dentro do pacote 'backend.app.database'.
# Isso evita qualquer ambiguidade e não depende do __init__.py.
from backend.app.database.connect_db import Base, engine

# Importa os roteadores que vamos usar.
from backend.app.routers import tasks_router

# Garante que as tabelas definidas em models.py existam no sofia_db
print("Verificando e criando tabelas do banco de dados, se necessário...")
Base.metadata.create_all(bind=engine)
print("✅ Verificação do banco de dados concluída.")


app = FastAPI(title="SOFIA Backend v3.2 - Estrutura Limpa")

# Inclui o roteador de tarefas na aplicação
app.include_router(tasks_router.router)

@app.get("/health", tags=["Health Check"])
def health_check():
    """Verifica se o serviço está online."""
    return {"status": "ok", "message": "SOFIA Backend online."}

