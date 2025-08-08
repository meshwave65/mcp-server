# engine/backend/app/models/models.py
# VERSÃO: 1.3 - Correção de Importação do DB

from sqlalchemy import Column, Integer, String, Text, Enum, DateTime, ForeignKey
from sqlalchemy.sql import func

# --- CORREÇÃO CRÍTICA ---
# Importa a Base declarativa do módulo 'connect_db.py' dentro do pacote 'database'.
from ..database.connect_db import Base

class Task(Base):
    __tablename__ = "tasks"
    task_id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    status = Column(Enum('pending', 'in_progress', 'completed', 'cancelled'), default='pending')
    priority = Column(Enum('low', 'medium', 'high', 'urgent'), default='medium')
    parent_task_id = Column(Integer, ForeignKey('tasks.task_id'), nullable=True)
    wbs_tag = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class MetadataType(Base):
    __tablename__ = "metadata_types"
    metadata_type_id = Column(Integer, primary_key=True)
    type_name = Column(String(255), nullable=False, unique=True)
    description = Column(Text, nullable=True)

class MetadataValue(Base):
    __tablename__ = "metadata_values"
    metadata_value_id = Column(Integer, primary_key=True)
    metadata_type_id = Column(Integer, ForeignKey('metadata_types.metadata_type_id'), nullable=False)
    value = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

class TaskMetadata(Base):
    __tablename__ = "task_metadata"
    task_id = Column(Integer, ForeignKey('tasks.task_id'), primary_key=True)
    metadata_value_id = Column(Integer, ForeignKey('metadata_values.metadata_value_id'), primary_key=True)

class TaskHistory(Base):
    __tablename__ = "task_history"
    history_id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey('tasks.task_id'), nullable=False)
    event_type = Column(String(100), nullable=False)
    old_value = Column(Text, nullable=True)
    new_value = Column(Text, nullable=True)
    event_timestamp = Column(DateTime, default=func.now())
    changed_by = Column(String(255), nullable=True)

