# sofia/backend/app/database/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

# --- CORREÇÃO AQUI ---
SQLALCHEMY_DATABASE_URL = os.getenv("SOFIA_DATABASE_URL")

if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("A variável de ambiente SOFIA_DATABASE_URL não foi definida!")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

