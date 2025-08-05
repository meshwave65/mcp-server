# sofia/backend/app/services/tasks_service.py (Versão SQL Puro - Estável)
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional, List, Dict

# --- CORREÇÃO AQUI: Importação Explícita e Direta ---
# Embora estejamos usando SQL puro, a importação do modelo é mantida
# para referência e para possíveis usos futuros do ORM.
from backend.app.models.task import Task

def get_all_tasks(
    db: Session,
    status: Optional[str] = None,
    agent_specialization_code: Optional[int] = None
) -> List[Dict]:
    """
    Lê todas as tarefas do banco de dados usando uma consulta SQL pura e segura.
    """
    try:
        query_sql = "SELECT * FROM tasks WHERE 1=1"
        params = {}

        if status is not None:
            query_sql += " AND status = :status"
            params["status"] = status
        
        if agent_specialization_code is not None:
            query_sql += " AND agent_specialization_code = :agent_specialization_code"
            params["agent_specialization_code"] = agent_specialization_code

        query_sql += " ORDER BY priority ASC, id ASC"

        result = db.execute(text(query_sql), params)
        tasks = [row._asdict() for row in result.mappings().all()]
        
        print(f"--- ✅ Sucesso! Encontradas {len(tasks)} tarefas no banco de dados. ---")
        return tasks

    except Exception as e:
        print(f"❌ ERRO CRÍTICO ao buscar tarefas com SQL puro: {e}")
        return []

# --- Funções Placeholders ---
def create_task(db: Session, task_data: dict) -> dict:
    raise NotImplementedError("Criação de tarefa via DB não implementada.")

def update_task(db: Session, task_id: int, update_data: dict) -> dict:
    raise NotImplementedError("Atualização de tarefa via DB não implementada.")

