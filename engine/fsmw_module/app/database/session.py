# ~/home/sofia/fsmw_module/app/database/session.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Lê a variável de ambiente específica para o banco de dados do FSMW
FSMW_DATABASE_URL = os.getenv("FSMW_DATABASE_URL")

if not FSMW_DATABASE_URL:
    raise ValueError("A variável de ambiente FSMW_DATABASE_URL não foi definida!")

engine = create_engine(FSMW_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

