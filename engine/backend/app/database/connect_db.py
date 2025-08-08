# engine/backend/app/database/connect_db.py
# SERVIÇO: Backend Principal SOFIA
# BANCO DE DADOS: sofia_db

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import sys

# Importa a URL do nosso ponto de verdade, o architecture.py
from architecture import SOFIA_DB_URL

# Validação crítica: impede a execução se a URL do DB não for encontrada.
if not SOFIA_DB_URL:
    print("❌ ERRO CRÍTICO: A variável SOFIA_DATABASE_URL não foi encontrada.")
    sys.exit(1)

engine = create_engine(SOFIA_DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Função padronizada para obter a sessão deste serviço.
def get_sofia_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

