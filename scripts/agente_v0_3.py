# agente_v0_3.py - Agente com Seleção por Prioridade para a API SOFIA v2.1

import requests
import time
import json

# --- Configurações ---
API_BASE_URL = "http://localhost:8000/api/v1"
AGENT_ID = "Agente-Manus-v0.3"

def print_json(data, title="" ):
    """Função auxiliar para imprimir JSON de forma legível."""
    if title:
        print(f"--- {title} ---")
    print(json.dumps(data, indent=2, ensure_ascii=False))

def run_agent():
    """
    Executa o ciclo de vida completo do Agente v0.3.
    """
    print(f"--- INICIANDO {AGENT_ID} ---")

    # 1. DESCOBRIR TAREFAS ABERTAS, ORDENADAS POR PRIORIDADE
    print("\n[PASSO 1] Procurando por tarefas 'open', ordenadas por prioridade...")
    try:
        # A chamada agora inclui o novo parâmetro para ordenar por prioridade
        response = requests.get(f"{API_BASE_URL}/tasks?status=open&sort_by_priority=true")
        response.raise_for_status()
        open_tasks = response.json()
    except requests.exceptions.RequestException as e:
        print(f"ERRO: Falha ao buscar tarefas. O backend está rodando? Detalhes: {e}")
        return

    if not open_tasks:
        print("RESULTADO: Nenhuma tarefa 'open' encontrada. Encerrando.")
        return

    # Seleciona a primeira tarefa da lista (que agora é a de maior prioridade)
    target_task_summary = open_tasks[0]
    task_id = target_task_summary['id']
    print(f"RESULTADO: Tarefa de maior prioridade encontrada. ID: {task_id}, Título: '{target_task_summary['title']}', Prioridade: {target_task_summary['priority']}")

    # 2. ASSUMIR A TAREFA
    print(f"\n[PASSO 2] Assumindo a tarefa {task_id}...")
    payload = {"status": "in_progress", "assigned_to": AGENT_ID}
    try:
        response = requests.patch(f"{API_BASE_URL}/tasks/{task_id}", json=payload)
        response.raise_for_status()
        print("RESULTADO: Tarefa assumida com sucesso.")
    except requests.exceptions.RequestException as e:
        print(f"ERRO: Falha ao assumir a tarefa. Detalhes: {e}")
        return

    # 3. ANALISAR DETALHES DA TAREFA
    print(f"\n[PASSO 3] Buscando detalhes e blocos da tarefa {task_id}...")
    try:
        response = requests.get(f"{API_BASE_URL}/tasks/{task_id}")
        response.raise_for_status()
        task_details = response.json()
        print("RESULTADO: Detalhes da tarefa obtidos com sucesso.")
        if task_details.get('blocks'):
            print(f"MISSÃO (do Bloco 0): {task_details['blocks'][0]['content']}")
        else:
            print("AVISO: A tarefa não possui blocos de conteúdo.")
    except requests.exceptions.RequestException as e:
        print(f"ERRO: Falha ao buscar detalhes da tarefa. Detalhes: {e}")
        return
            
    # 4. RELATAR PROGRESSO
    print(f"\n[PASSO 4] Adicionando um novo bloco de progresso à tarefa {task_id}...")
    progress_content = "Análise de prioridade confirmada. Iniciando execução da tarefa mais urgente."
    payload = {
        "author_id": AGENT_ID,
        "block_type": "ProgressUpdate",
        "content": progress_content
    }
    try:
        response = requests.post(f"{API_BASE_URL}/tasks/{task_id}/blocks", json=payload)
        response.raise_for_status()
        print("RESULTADO: Novo bloco de progresso adicionado com sucesso.")
    except requests.exceptions.RequestException as e:
        print(f"ERRO: Falha ao adicionar novo bloco. Detalhes: {e}")
        return

    # 5. COMPLETAR A TAREFA
    print(f"\n[PASSO 5] Completando a tarefa {task_id}...")
    payload = {"status": "done"}
    try:
        response = requests.patch(f"{API_BASE_URL}/tasks/{task_id}", json=payload)
        response.raise_for_status()
        print("RESULTADO: Tarefa completada com sucesso!")
    except requests.exceptions.RequestException as e:
        print(f"ERRO: Falha ao completar a tarefa. Detalhes: {e}")
        return

    print(f"\n--- CICLO DO {AGENT_ID} CONCLUÍDO COM SUCESSO ---")

if __name__ == "__main__":
    run_agent()

