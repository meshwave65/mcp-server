# main.py - Implementação do Backend SOFIA v2 com FastAPI

from fastapi import FastAPI, HTTPException, Depends, Query
from pydantic import BaseModel
from typing import List, Optional
import mysql.connector
import uuid
from contextlib import contextmanager

# --- Configuração do Banco de Dados ---
# IMPORTANTE: Ajuste 'user' e 'password' conforme sua configuração local.
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'A_SUA_SENHA_SECRETA_AQUI', # <-- COLOQUE SUA SENHA AQUI
    'database': 'meshwave_db'
}

# --- Gerenciador de Conexão com o Banco de Dados ---
@contextmanager
def get_db_connection():
    """Gerencia a conexão com o banco de dados de forma segura."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        yield conn
    finally:
        if 'conn' in locals() and conn.is_connected():
            conn.close()

# --- Modelos Pydantic (para validação de dados) ---
class TaskBase(BaseModel):
    id: int
    title: str
    status: str
    priority: int
    assigned_to: Optional[str] = None

class BlockBase(BaseModel):
    sequence: int
    block_type: str
    author_id: str
    content: str

class TaskDetails(TaskBase):
    original_task_id: Optional[str] = None
    blocks: List[BlockBase]

class TaskUpdate(BaseModel):
    status: Optional[str] = None
    priority: Optional[int] = None
    assigned_to: Optional[str] = None

class BlockCreate(BaseModel):
    author_id: str
    block_type: str
    content: str

# --- Inicialização da Aplicação FastAPI ---
app = FastAPI(
    title="SOFIA Backend API",
    version="2.0.0",
    description="API para o sistema SOFIA e seus projetos gerenciados, conectada à arquitetura de DB v2."
)

# --- Implementação dos Endpoints ---

@app.get("/api/v1/tasks", response_model=List[TaskBase], tags=["Tasks"])
def read_all_tasks(status: Optional[str] = Query(None, description="Filtra tarefas por status (ex: open, in_progress)")):
    """
    Lista as tarefas principais. Suporta filtragem por status.
    """
    query = "SELECT id, title, status, priority, assigned_to FROM tasks"
    params = []
    if status:
        query += " WHERE status = %s"
        params.append(status)
    
    with get_db_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, tuple(params))
        tasks = cursor.fetchall()
    return tasks

@app.get("/api/v1/tasks/{task_id}", response_model=TaskDetails, tags=["Tasks"])
def read_task_details(task_id: int):
    """
    Obtém os detalhes completos de uma única tarefa, incluindo todos os seus blocos.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        
        # Busca metadados da tarefa
        cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
        task = cursor.fetchone()
        if not task:
            raise HTTPException(status_code=404, detail="Tarefa não encontrada")
            
        # Busca os blocos da tarefa
        cursor.execute("SELECT sequence, block_type, author_id, content FROM TaskBlocks WHERE task_id = %s ORDER BY sequence ASC", (task_id,))
        blocks = cursor.fetchall()
        
        task['blocks'] = blocks
    return task

@app.patch("/api/v1/tasks/{task_id}", response_model=TaskBase, tags=["Tasks"])
def update_task(task_id: int, task_update: TaskUpdate):
    """
    Atualiza os metadados de uma tarefa (status, prioridade, etc.).
    """
    update_fields = task_update.dict(exclude_unset=True)
    if not update_fields:
        raise HTTPException(status_code=400, detail="Nenhum campo para atualizar fornecido.")

    set_clause = ", ".join([f"{key} = %s" for key in update_fields.keys()])
    params = list(update_fields.values())
    params.append(task_id)

    query = f"UPDATE tasks SET {set_clause} WHERE id = %s"

    with get_db_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, tuple(params))
        conn.commit()
        
        # Retorna a tarefa atualizada
        cursor.execute("SELECT id, title, status, priority, assigned_to FROM tasks WHERE id = %s", (task_id,))
        updated_task = cursor.fetchone()
    return updated_task

@app.post("/api/v1/tasks/{task_id}/blocks", response_model=BlockBase, tags=["Tasks"])
def create_block_for_task(task_id: int, block: BlockCreate):
    """
    Adiciona um novo bloco a uma tarefa existente.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        
        # Calcula o próximo sequence
        cursor.execute("SELECT MAX(sequence) as max_seq FROM TaskBlocks WHERE task_id = %s", (task_id,))
        result = cursor.fetchone()
        next_sequence = (result['max_seq'] or -1) + 1
        
        new_block_id = str(uuid.uuid4())
        
        query = """
        INSERT INTO TaskBlocks (block_id, task_id, sequence, author_id, block_type, content)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (new_block_id, task_id, next_sequence, block.author_id, block.block_type, block.content)
        
        cursor.execute(query, params)
        conn.commit()
        
    return {"sequence": next_sequence, **block.dict()}

# --- Comando para rodar o servidor (para referência) ---
# uvicorn main:app --reload

