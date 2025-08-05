# sofia/backend/app/database/base.py
from sqlalchemy.ext.declarative import declarative_base

# Cria uma classe Base que será usada por todos os seus modelos ORM
# para herdar a funcionalidade do SQLAlchemy.
Base = declarative_base()

