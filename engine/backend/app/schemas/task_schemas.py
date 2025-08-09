# engine/backend/app/schemas/task_schemas.py
# VERSÃO: 5.4 - Modernizando para Pydantic v2 (from_attributes)

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class TaskCreateModel(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Optional[str] = 'medium'
    parent_task_id: Optional[int] = None
    wbs_tag: str

class TaskUpdateModel(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None

class TaskResponseModel(BaseModel):
    task_id: int
    title: str
    description: Optional[str] = None
    status: str
    priority: str
    wbs_tag: str
    created_at: datetime
    updated_at: datetime
    parent_task_id: Optional[int] = None

    class Config:
        # orm_mode = True  <-- Linha antiga
        from_attributes = True # <-- Nova sintaxe recomendada para Pydantic v2+

