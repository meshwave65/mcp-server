# sofia/fsmw_module/app/database/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Pega a URL de conexão específica do FSMW do arquivo .env
FSMW_DATABASE_URL = os.getenv("FSMW_DATABASE_URL")
if not FSMW_DATABASE_URL:
    raise ValueError("A variável de ambiente FSMW_DATABASE_URL não foi definida no arquivo .env!")

# Cria o 'motor' de conexão para o banco de dados do FSMW
engine = create_engine(FSMW_DATABASE_URL)

# Cria uma fábrica de sessões que será usada para criar sessões individuais
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_fsmw_db():
    """
    Função de dependência do FastAPI para obter uma sessão do banco de dados FSMW.
    Garante que a sessão seja sempre fechada após a requisição.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

