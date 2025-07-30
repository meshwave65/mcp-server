# sofia/engine/backend/app/database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# String de conexão para o seu banco de dados MySQL 'meshwave_db'.
# Formato: "mysql+pymysql://<user>:<password>@<host>/<dbname>"
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:mesh1234@localhost/meshwave_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

