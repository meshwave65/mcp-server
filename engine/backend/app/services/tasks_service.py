# engine/backend/app/services/tasks_service.py
# VERSÃO: 3.1 - Lógica de DB com ORM e Injeção de Dependência

from sqlalchemy.orm import Session
from sqlalchemy import case
from typing import List, Optional

# Importa o modelo de dados e os schemas Pydantic
from ..models.models import Task
from ..schemas import task_schemas

def create_task(db: Session, task_data: task_schemas.TaskCreateModel) -> Task:
    """Cria uma nova tarefa no banco de dados usando o ORM."""
    new_task = Task(**task_data.model_dump())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

def get_all_tasks(db: Session, status: Optional[str], sort_by: str) -> List[Task]:
    """Lê as tarefas do banco de dados usando o ORM."""
    query = db.query(Task)
    if status:
        query = query.filter(Task.status == status)

    if sort_by == 'priority':
        priority_order = case(
            (Task.priority == 'urgent', 0),
            (Task.priority == 'high', 1),
            (Task.priority == 'medium', 2),
            (Task.priority == 'low', 3),
            else_=4
        )
        query = query.order_by(priority_order, Task.created_at.desc())
    else:
        query = query.order_by(Task.created_at.desc())

    return query.all()

def update_task(db: Session, task_id: int, update_data: task_schemas.TaskUpdateModel) -> Optional[Task]:
    """Atualiza uma tarefa existente no banco de dados."""
    task_to_update = db.query(Task).filter(Task.task_id == task_id).first()
    if not task_to_update:
        return None

    update_dict = update_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(task_to_update, key, value)

    db.commit()
    db.refresh(task_to_update)
    return task_to_update

