# engine/backend/app/routers/tasks_router.py
# VERSÃO: 5.2 - ESTÁVEL (CRUD Completo)

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from ..services import tasks_service
from ..schemas import task_schemas
from ..database.connect_db import get_sofia_db

router = APIRouter(
    prefix="/api/v1/tasks",
    tags=["Tasks"]
)

@router.post("/", response_model=task_schemas.TaskResponseModel, status_code=201)
def create_task(task: task_schemas.TaskCreateModel, db: Session = Depends(get_sofia_db)):
    return tasks_service.create_task(db=db, task_data=task)

@router.get("/", response_model=List[task_schemas.TaskResponseModel])
def read_all_tasks(
    status: Optional[str] = Query(None, description="Filtrar por status"),
    sort_by: str = Query("priority", enum=["priority", "created_at"]),
    db: Session = Depends(get_sofia_db)
):
    return tasks_service.get_all_tasks(db=db, status=status, sort_by=sort_by)

@router.patch("/{task_id}", response_model=task_schemas.TaskResponseModel)
def update_task(
    task_id: int,
    task_update: task_schemas.TaskUpdateModel,
    db: Session = Depends(get_sofia_db)
):
    updated_task = tasks_service.update_task(db=db, task_id=task_id, update_data=task_update)
    if updated_task is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return updated_task

