# sofia/backend/app/models/task.py (Versão Final Sincronizada)
from sqlalchemy import Column, Integer, String, Text

# Importa a Base do nosso arquivo de banco de dados
from backend.app.database.base import Base

class Task(Base):
    __tablename__ = "tasks"

    # Colunas que existem na sua tabela, com os tipos corretos
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True) # Permite valores nulos (NULL)
    status = Column(String(50), default="open")
    priority = Column(Integer, default=3)
    assigned_to = Column(String(255), nullable=True)
    original_task_id = Column(String(255), nullable=True)
    agent_specialization_code = Column(Integer, nullable=True)

