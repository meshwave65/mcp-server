# engine/backend/app/models/models.py
# VERSÃO: 5.1 - SINCRONIZAÇÃO FINAL E COMPLETA

from sqlalchemy import Column, Integer, String, Text, Enum, DateTime, ForeignKey
from sqlalchemy.sql import func
from ..database.connect_db import Base

class Task(Base):
    """
    Modelo SQLAlchemy que representa a tabela 'tasks'.
    """
    __tablename__ = "tasks"

    task_id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    
    # --- CORREÇÃO CRÍTICA ---
    # Adicionando a coluna 'description' que estava faltando na classe Task.
    description = Column(Text, nullable=True)
    
    status = Column(Enum('pending', 'in_progress', 'completed', 'cancelled'), default='pending')
    priority = Column(Enum('low', 'medium', 'high', 'urgent'), default='medium')
    parent_task_id = Column(Integer, ForeignKey('tasks.task_id'), nullable=True)
    wbs_tag = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class MetadataType(Base):
    """
    Modelo para a tabela 'metadata_types'.
    """
    __tablename__ = "metadata_types"

    metadata_type_id = Column(Integer, primary_key=True)
    type_name = Column(String(255), nullable=False, unique=True)
    description = Column(Text, nullable=True)

class MetadataValue(Base):
    """
    Modelo para a tabela 'metadata_values'.
    """
    __tablename__ = "metadata_values"

    metadata_value_id = Column(Integer, primary_key=True)
    metadata_type_id = Column(Integer, ForeignKey('metadata_types.metadata_type_id'), nullable=False)
    value = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

class TaskMetadata(Base):
    """
    Modelo para a tabela de junção 'task_metadata'.
    """
    __tablename__ = "task_metadata"

    task_id = Column(Integer, ForeignKey('tasks.task_id'), primary_key=True)
    metadata_value_id = Column(Integer, ForeignKey('metadata_values.metadata_value_id'), primary_key=True)

class TaskHistory(Base):
    """
    Modelo para a tabela 'task_history'.
    """
    __tablename__ = "task_history"

    history_id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey('tasks.task_id'), nullable=False)
    event_type = Column(String(100), nullable=False)
    old_value = Column(Text, nullable=True)
    new_value = Column(Text, nullable=True)
    event_timestamp = Column(DateTime, default=func.now())
    changed_by = Column(String(255), nullable=True)

