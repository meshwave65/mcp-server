# engine/backend/app/schemas/task_schemas.py
# VERSÃO: 1.0 - Definição dos Contratos de Dados para Tarefas

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Schema para a criação de uma nova tarefa.
# Define os campos que o cliente DEVE enviar.
class TaskCreateModel(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Optional[str] = 'medium'
    parent_task_id: Optional[int] = None
    wbs_tag: str

# Schema para a atualização de uma tarefa.
# Todos os campos são opcionais, pois o cliente pode querer atualizar apenas um.
class TaskUpdateModel(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    parent_task_id: Optional[int] = None
    wbs_tag: Optional[str] = None

# Schema para a resposta da API.
# Define os campos que o servidor SEMPRE enviará de volta.
# Inclui o 'orm_mode' para permitir que o Pydantic leia dados de objetos SQLAlchemy.
class TaskResponseModel(BaseModel):
    task_id: int
    title: str
    status: str
    priority: str
    wbs_tag: str
    created_at: datetime
    updated_at: datetime
    parent_task_id: Optional[int] = None

    class Config:
        from_attributes = True # Substitui o 'orm_mode = True' obsoleto

