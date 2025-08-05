# sofia/backend/fsmw_module/app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# --- CORREÇÃO AQUI ---
FSMW_SQLALCHEMY_DATABASE_URL = os.getenv("FSMW_DATABASE_URL")

if not FSMW_SQLALCHEMY_DATABASE_URL:
    raise ValueError("A variável de ambiente FSMW_DATABASE_URL não foi definida!")

# Cria uma engine separada para o banco de dados do FSMW
fsmw_engine = create_engine(FSMW_SQLALCHEMY_DATABASE_URL)
FsmwSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=fsmw_engine)

def get_fsmw_db_session():
    """
    Cria e retorna uma nova sessão para o banco de dados do FSMW.
    """
    db = FsmwSessionLocal()
    try:
        yield db # Para uso futuro com dependências Flask
        # Por enquanto, vamos retornar a sessão diretamente para compatibilidade
        return db
    finally:
        db.close()

