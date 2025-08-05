# sofia/backend/app/routes/tasks_router.py (Refatorado)
from fastapi import APIRouter, HTTPException, status, Query, Depends
from sqlalchemy.orm import Session
from typing import Dict, Optional, List

# Importa o serviço correspondente
from backend.app.services import tasks_service
from backend.app.database import get_db

router = APIRouter(
    prefix="/api/v1/tasks",
    tags=["Tasks"]
)

@router.get("/", response_model=List[Dict])
def read_all_tasks(
    db: Session = Depends(get_db),
    status: Optional[str] = Query(None),
    agent_specialization_code: Optional[int] = Query(None)
):
    """
    Lista todas as tarefas do banco de dados com filtros.
    A lógica agora está no serviço.
    """
    try:
        tasks = tasks_service.get_all_tasks(
            db=db,
            status=status,
            agent_specialization_code=agent_specialization_code
        )
        return tasks
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno ao listar tarefas: {e}")

# As rotas de criação e atualização ainda chamam os placeholders, o que está correto.
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_new_task(task_data: Dict, db: Session = Depends(get_db)):
    try:
        return tasks_service.create_task(db=db, task_data=task_data)
    except NotImplementedError:
        raise HTTPException(status_code=501, detail="Funcionalidade de criação de tarefa não implementada.")

@router.patch("/{task_id}", response_model=Dict)
def update_existing_task(task_id: int, update_data: Dict, db: Session = Depends(get_db)):
    try:
        return tasks_service.update_task(db=db, task_id=task_id, update_data=update_data)
    except NotImplementedError:
        raise HTTPException(status_code=501, detail="Funcionalidade de atualização de tarefa não implementada.")

