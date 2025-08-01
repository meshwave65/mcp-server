# main.py (v2.2.2 - CORRIGIDO)
# Corrige a falha na criação de blocos (faltava o block_id).

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
import mysql.connector
from contextlib import contextmanager
from typing import List, Optional
import uuid # <-- IMPORTANTE: Adicionamos a biblioteca uuid

# --- Configuração do Banco de Dados ---
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'mesh1234', # Sua senha
    'database': 'meshwave_db'
}

# --- Modelos Pydantic (Estruturas de Dados) ---
class Task(BaseModel):
    id: int
    title: str
    status: str
    priority: int
    assigned_to: Optional[str] = None

class TaskBlock(BaseModel):
    sequence: int
    block_type: str
    author_id: str
    content: str

class TaskDetail(Task):
    blocks: List[TaskBlock]

# --- Context Manager para Conexão com o DB ---
@contextmanager
def get_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        yield conn
    finally:
        if 'conn' in locals() and conn.is_connected():
            conn.close()

# --- Inicialização da Aplicação FastAPI ---
app = FastAPI(
    title="SOFIA Task Management API",
    description="API para gerenciar tarefas e agentes no ecossistema SOFIA.",
    version="2.2.2",
)

# --- Endpoint do Oráculo ---
@app.get("/oracle", response_class=PlainTextResponse, tags=["Oracle"])
def get_oracle():
    try:
        with open("SOFIA_OPERATIONS_MANUAL.md", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Manual de Operações (Oráculo) não encontrado.")

# --- Endpoints da API ---
@app.get("/api/v1/tasks", response_model=List[Task], tags=["Tasks"])
def get_tasks(status: Optional[str] = None, sort_by_priority: bool = False):
    with get_db_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT id, title, status, priority, assigned_to FROM tasks"
        params = []
        if status:
            query += " WHERE status = %s"
            params.append(status)
        if sort_by_priority:
            query += " ORDER BY priority ASC" # Prioridade 1 é a mais alta
        
        cursor.execute(query, tuple(params))
        tasks = cursor.fetchall()
        return tasks

@app.get("/api/v1/tasks/{task_id}", response_model=TaskDetail, tags=["Tasks"])
def get_task_details(task_id: int):
    with get_db_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        
        # Busca a tarefa principal
        cursor.execute("SELECT id, title, status, priority, assigned_to FROM tasks WHERE id = %s", (task_id,))
        task = cursor.fetchone()
        if not task:
            raise HTTPException(status_code=404, detail="Tarefa não encontrada")
            
        # Busca os blocos da tarefa
        cursor.execute("SELECT sequence, block_type, author_id, content FROM TaskBlocks WHERE task_id = %s ORDER BY sequence ASC", (task_id,))
        blocks = cursor.fetchall()
        
        task['blocks'] = blocks
        return task

@app.patch("/api/v1/tasks/{task_id}", response_model=Task, tags=["Tasks"])
def update_task_status(task_id: int, update_data: dict):
    with get_db_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        
        # Constrói a query de update dinamicamente
        set_clauses = []
        params = []
        for key, value in update_data.items():
            set_clauses.append(f"{key} = %s")
            params.append(value)
        
        if not set_clauses:
            raise HTTPException(status_code=400, detail="Nenhum dado para atualizar")

        query = f"UPDATE tasks SET {', '.join(set_clauses)} WHERE id = %s"
        params.append(task_id)
        
        cursor.execute(query, tuple(params))
        conn.commit()
        
        # Retorna a tarefa atualizada
        cursor.execute("SELECT id, title, status, priority, assigned_to FROM tasks WHERE id = %s", (task_id,))
        updated_task = cursor.fetchone()
        return updated_task

@app.post("/api/v1/tasks/{task_id}/blocks", response_model=TaskBlock, tags=["Tasks"])
def create_task_block(task_id: int, new_block: TaskBlock):
    with get_db_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        
        # --- INÍCIO DA CORREÇÃO ---
        # Geramos um UUID para o novo bloco
        new_block_id = str(uuid.uuid4())
        
        query = """
            INSERT INTO TaskBlocks (block_id, task_id, sequence, author_id, block_type, content)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        # Adicionamos o new_block_id aos parâmetros
        params = (new_block_id, task_id, new_block.sequence, new_block.author_id, new_block.block_type, new_block.content)
        # --- FIM DA CORREÇÃO ---
        
        try:
            cursor.execute(query, params)
            conn.commit()
            return new_block
        except mysql.connector.Error as e:
            # Log do erro no servidor para depuração
            print(f"Erro de banco de dados ao criar bloco: {e}")
            raise HTTPException(status_code=500, detail=f"Erro interno ao criar bloco: {e}")


