# sofia/engine/backend/app/routers/tasks_router.py

from fastapi import APIRouter, HTTPException, status
from typing import Dict, Optional, List

# Importa o serviço e o modelo de dados que criamos
# Importa o serviço e o modelo de dados
from ..services.tasks_service import create_task, get_all_tasks, update_task
from ..services.tasks_service import TaskCreateModel  # Importação corrigida
from ..services.tasks_service import TaskUpdateModel  # Modelo de atualização

# Cria uma instância do roteador.
# O prefixo garante que todos os endpoints aqui comecem com /api/v1/tasks
# A tag agrupa os endpoints na documentação interativa do FastAPI.
router = APIRouter(
    prefix="/api/v1/tasks",
    tags=["Tasks"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_new_task(task_data: TaskCreateModel) -> Dict:
    """
    Cria uma nova tarefa no sistema.

    Recebe um corpo JSON com os seguintes campos:
    - **title**: O título da tarefa (string, obrigatório).
    - **description**: A descrição detalhada da tarefa (string, obrigatório).
    - **priority**: Nível de prioridade (inteiro, 1-4, padrão: 2).
    - **due_date**: Data limite para a conclusão (string de data/hora ISO, opcional).
    - **tags**: Uma lista de tags (array de strings, opcional).
    - **project**: Nome do projeto associado (string, opcional).
    - **module_id**: ID do módulo associado (inteiro, opcional).
    """
    
    # Chama a função do nosso serviço para fazer o trabalho pesado
    result = tasks_service.create_task(task_data)

    # Verifica se o serviço retornou um erro
    if "error" in result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Falha ao criar a tarefa: {result['error']}"
        )
    
    # Se tudo correu bem, retorna os metadados da tarefa criada
    return result

# Adicione esta função ao seu arquivo tasks_router.py

from fastapi import Query # Importe o Query para validação avançada
from typing import List # Importe o List para o tipo de retorno

# ... (mantenha a função create_new_task que já existe) ...

@router.get("/", response_model=List[Dict])
def read_all_tasks(
    status_agente: Optional[int] = Query(None, description="Filtrar por status do agente (ex: 1 para Open)"),
    assigned_to: Optional[str] = Query(None, description="Filtrar por agente designado"),
    sort_by: str = Query('priority', enum=['priority', 'created_at'], description="Ordenar por 'priority' ou 'created_at'")
):
    """
    Lista todas as tarefas, com opções de filtro e ordenação.
    Ideal para agentes encontrarem novas tarefas ou para painéis de visualização.
    """
    tasks = tasks_service.get_all_tasks(
        status_agente=status_agente,
        assigned_to=assigned_to,
        sort_by=sort_by
    )
    return tasks

# Adicione esta função ao final do seu arquivo tasks_router.py

# Importe o modelo de atualização que acabamos de criar
from ..services.tasks_service import TaskUpdateModel
#from app.services.tasks_service import TaskUpdateModel

# ... (mantenha as funções create_new_task e read_all_tasks) ...

@router.patch("/{task_id}", response_model=Dict)
def update_existing_task(task_id: str, update_data: TaskUpdateModel):
    """
    Atualiza uma tarefa existente executando uma ação específica.
    Este é o endpoint principal para os agentes interagirem com as tarefas.

    - **task_id**: O ID da tarefa a ser atualizada (ex: TSK-20250730-001).
    - **Request Body**: Um JSON com:
        - **action_type**: A ação a ser executada (ex: "ASSIGN_TO_SELF").
        - **payload**: Um dicionário com dados adicionais para a ação 
          (ex: `{"agent_id": "IA-Agente-007"}`).
    """
    result = tasks_service.update_task(task_id, update_data)

    if "error" in result:
        status_code = result.get("status_code", 500)
        raise HTTPException(
            status_code=status_code,
            detail=result["error"]
        )
    
    return result




