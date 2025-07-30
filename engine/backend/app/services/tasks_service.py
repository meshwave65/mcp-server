# sofia/engine/backend/app/services/tasks_service.py

import frontmatter
import os
from pathlib import Path
from datetime import datetime, timezone
from pydantic import BaseModel, Field
from typing import Optional, List, Dict

# --- Definição do Modelo de Dados para a Criação da Tarefa ---
# Isso garante que os dados recebidos pela API tenham a estrutura correta.
class TaskCreateModel(BaseModel):
    title: str
    description: str
    priority: int = Field(default=2, ge=1, le=4) # ge=greater or equal, le=less or equal
    due_date: Optional[datetime] = None
    tags: Optional[List[str]] = []
    project: Optional[str] = "DefaultProject"
    module_id: Optional[int] = None


# --- Configuração do Diretório de Tarefas ---
# Usamos Path para lidar com caminhos de forma mais robusta.
TASKS_DIR = Path("tasks")

# Garante que o diretório /tasks exista ao iniciar.
TASKS_DIR.mkdir(exist_ok=True)


def generate_task_id() -> str:
    """
    Gera um ID de tarefa único baseado na data e um contador diário.
    Formato: TSK-YYYYMMDD-NNN
    """
    today_str = datetime.now(timezone.utc).strftime("%Y%m%d")
    counter = 1
    while True:
        task_id = f"TSK-{today_str}-{counter:03d}"
        if not (TASKS_DIR / f"{task_id}.md").exists():
            return task_id
        counter += 1


def create_task(task_data: TaskCreateModel) -> dict:
    """
    Cria um novo arquivo de tarefa .md com base nos dados fornecidos.
    """
    try:
        task_id = generate_task_id()
        now_utc = datetime.now(timezone.utc)

        # 1. Define os metadados (cabeçalho YAML)
        metadata = {
            'task_id': task_id,
            'title': task_data.title,
            'project': task_data.project,
            'module_id': task_data.module_id,
            'status_agente': 1,  # 1: Open
            'turn_holder': 0,    # 0: Agente
            'priority': task_data.priority,
            'assigned_to': 'any',
            'created_at': now_utc.isoformat(),
            'updated_at': now_utc.isoformat(),
            'due_date': task_data.due_date.isoformat() if task_data.due_date else None,
            'tags': task_data.tags,
            'estimated_effort_hours': 8 # Valor padrão inicial
        }

        # 2. Define o conteúdo inicial do Markdown
        content = f"# {task_data.title}\n\n"
        content += "## Descrição Inicial da Tarefa\n"
        content += f"> {task_data.description}\n\n"
        content += "---\n"
        content += f"### Bloco de Interação: {now_utc.isoformat()} | Sistema\n"
        content += "**Ação:** Tarefa Criada\n"
        content += "**Mudança de Estado:** status_agente: 0 -> 1 | turn_holder: 0 -> 0\n"

        # 3. Cria o objeto Post com metadados e conteúdo
        post = frontmatter.Post(content, **metadata)

        # 4. Define o caminho completo do arquivo
        file_path = TASKS_DIR / f"{task_id}.md"

        # 5. Salva o arquivo no disco
        with open(file_path, "wb") as f:
            frontmatter.dump(post, f)

        print(f"✅ Tarefa criada com sucesso: {file_path}")
        
        # Retorna os metadados da tarefa criada para a API
        return metadata

    except Exception as e:
        print(f"❌ ERRO CRÍTICO ao criar a tarefa: {e}")
        # Em um sistema real, aqui teríamos um log mais robusto.
        # Por enquanto, retornamos um dicionário de erro.
        return {"error": str(e)}

# Adicione esta função ao final do seu arquivo tasks_service.py

def get_all_tasks(
    status_agente: Optional[int] = None,
    assigned_to: Optional[str] = None,
    sort_by: str = 'priority' # 'priority' ou 'created_at'
) -> List[Dict]:
    """
    Lê todos os arquivos de tarefa do diretório, filtra e ordena conforme os parâmetros.
    """
    all_tasks = []
    
    # 1. Itera sobre todos os arquivos .md no diretório de tarefas
    for file_path in TASKS_DIR.glob("*.md"):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                post = frontmatter.load(f)
                # Adicionamos o conteúdo do arquivo também, caso seja útil no futuro
                task_data = post.metadata
                task_data['content'] = post.content
                all_tasks.append(task_data)
        except Exception as e:
            print(f"⚠️  Aviso: Falha ao ler ou processar o arquivo {file_path}: {e}")
            continue # Pula para o próximo arquivo em caso de erro

    # 2. Filtra os resultados com base nos parâmetros da query
    filtered_tasks = all_tasks
    if status_agente is not None:
        filtered_tasks = [t for t in filtered_tasks if t.get('status_agente') == status_agente]
    
    if assigned_to is not None:
        filtered_tasks = [t for t in filtered_tasks if t.get('assigned_to') == assigned_to]

    # 3. Ordena os resultados
    # A ordenação principal é por prioridade (maior para menor).
    # Como desempate, usamos a data de criação (mais antigo primeiro).
    if sort_by == 'priority':
        # `reverse=True` para que a maior prioridade (ex: 4) venha primeiro.
        filtered_tasks.sort(key=lambda t: (t.get('priority', 0), t.get('created_at', '')), reverse=True)
    else: # sort_by == 'created_at'
        filtered_tasks.sort(key=lambda t: t.get('created_at', ''))

    return filtered_tasks

# Adicione este novo código ao final do seu arquivo tasks_service.py

# --- Modelo de Dados para a Atualização da Tarefa ---
# Define a estrutura do corpo (body) da nossa requisição PATCH.
class TaskUpdateModel(BaseModel):
    action_type: str
    payload: Optional[Dict] = {}

# --- Função Principal de Atualização ---

def update_task(task_id: str, update_data: TaskUpdateModel) -> Dict:
    """
    Atualiza uma tarefa existente com base em uma ação específica.
    Esta é a função central para todas as interações dos agentes.
    """
    file_path = TASKS_DIR / f"{task_id}.md"

    # 1. Validação: Verifica se a tarefa existe
    if not file_path.exists():
        return {"error": "Task not found", "status_code": 404}

    try:
        # 2. Carrega o arquivo da tarefa
        with open(file_path, "r", encoding="utf-8") as f:
            post = frontmatter.load(f)

        # --- Lógica Central: O "Cérebro" do Sistema ---
        # Executa diferentes lógicas com base no tipo de ação recebido.
        
        action = update_data.action_type
        payload = update_data.payload
        now_utc_iso = datetime.now(timezone.utc).isoformat()
        
        interaction_block = ""

        if action == "ASSIGN_TO_SELF":
            agent_id = payload.get("agent_id", "unknown_agent")
            
            # Validação de regra de negócio
            if post.metadata.get('status_agente') != 1:
                 return {"error": "Task is not open. Cannot be assigned.", "status_code": 409} # 409 Conflict

            # Atualiza os metadados
            post.metadata['status_agente'] = 2  # 2: In_Progress
            post.metadata['assigned_to'] = agent_id
            
            # Cria o bloco de interação
            interaction_block = (
                f"### Bloco de Interação: {now_utc_iso} | {agent_id}\n"
                f"**Ação:** Tarefa Atribuída\n"
                f"**Mudança de Estado:** status_agente: 1 -> 2 | assigned_to: any -> {agent_id}\n"
            )

        # --- (Futuro) Outros tipos de ação virão aqui ---
        # elif action == "ASK_QUESTION":
        #     # Lógica para adicionar dúvida, mudar turn_holder, criar .link
        #     pass
        # elif action == "SUBMIT_FOR_REVIEW":
        #     # Lógica para submeter, mudar status, notificar gestor
        #     pass
        else:
            return {"error": f"Invalid action_type: {action}", "status_code": 400}

        # 3. Adiciona o novo bloco de interação ao conteúdo
        post.content += f"\n---\n{interaction_block}"
        
        # 4. Atualiza o timestamp de modificação
        post.metadata['updated_at'] = now_utc_iso

        # 5. Salva o arquivo modificado
        with open(file_path, "wb") as f:
            frontmatter.dump(post, f)

        print(f"✅ Tarefa atualizada com sucesso: {task_id}")
        return post.metadata

    except Exception as e:
        print(f"❌ ERRO CRÍTICO ao atualizar a tarefa {task_id}: {e}")
        return {"error": str(e), "status_code": 500}




