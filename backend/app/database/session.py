# sofia/backend/app/database/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Pega a URL de conexão do banco de dados a partir das variáveis de ambiente
SQLALCHEMY_DATABASE_URL = os.getenv("SOFIA_DATABASE_URL")

if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("A variável de ambiente SOFIA_DATABASE_URL não foi definida!")

# Cria a "engine" do SQLAlchemy
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

# Cria uma classe SessionLocal, que será a fábrica de sessões
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Função de Dependência para FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

