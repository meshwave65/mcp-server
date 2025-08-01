# agent_v0_2.py - Agente Inteligente para a API SOFIA v2

import requests
import time
import json

# --- Configurações ---
API_BASE_URL = "http://localhost:8000/api/v1"
AGENT_ID = "Agente-Manus-v0.2"

def print_json(data, title="" ):
    """Função auxiliar para imprimir JSON de forma legível."""
    if title:
        print(f"--- {title} ---")
    print(json.dumps(data, indent=2, ensure_ascii=False))

def run_agent():
    """
    Executa o ciclo de vida completo do Agente v0.2.
    """
    print(f"--- INICIANDO {AGENT_ID} ---")

    # 1. DESCOBRIR TAREFAS ABERTAS
    print("\n[PASSO 1] Procurando por tarefas com status 'open'...")
    try:
        response = requests.get(f"{API_BASE_URL}/tasks?status=open")
        response.raise_for_status()
        open_tasks = response.json()
    except requests.exceptions.RequestException as e:
        print(f"ERRO: Falha ao buscar tarefas. O backend está rodando? Detalhes: {e}")
        return

    if not open_tasks:
        print("RESULTADO: Nenhuma tarefa 'open' encontrada. Encerrando.")
        return

    # Seleciona a primeira tarefa da lista
    target_task_summary = open_tasks[0]
    task_id = target_task_summary['id']
    print(f"RESULTADO: Tarefa encontrada para processar. ID: {task_id}, Título: '{target_task_summary['title']}'")

    # 2. ASSUMIR A TAREFA
    print(f"\n[PASSO 2] Assumindo a tarefa {task_id}...")
    payload = {"status": "in_progress", "assigned_to": AGENT_ID}
    try:
        response = requests.patch(f"{API_BASE_URL}/tasks/{task_id}", json=payload)
        response.raise_for_status()
        print("RESULTADO: Tarefa assumida com sucesso.")
        print_json(response.json(), "Status da Tarefa Atualizado")
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
        # O agente "lê" a missão principal do primeiro bloco
        if task_details.get('blocks'):
            print(f"MISSÃO (do Bloco 0): {task_details['blocks'][0]['content']}")
        else:
            print("AVISO: A tarefa não possui blocos de conteúdo.")
    except requests.exceptions.RequestException as e:
        print(f"ERRO: Falha ao buscar detalhes da tarefa. Detalhes: {e}")
        return
        
    # 4. RELATAR PROGRESSO (ADICIONAR UM NOVO BLOCO)
    print(f"\n[PASSO 4] Adicionando um novo bloco de progresso à tarefa {task_id}...")
    progress_content = "Análise inicial da tarefa concluída. Próximo passo: detalhar o plano de execução."
    payload = {
        "author_id": AGENT_ID,
        "block_type": "ProgressUpdate",
        "content": progress_content
    }
    try:
        response = requests.post(f"{API_BASE_URL}/tasks/{task_id}/blocks", json=payload)
        response.raise_for_status()
        print("RESULTADO: Novo bloco de progresso adicionado com sucesso.")
        print_json(response.json(), "Bloco Criado")
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
        print_json(response.json(), "Status Final da Tarefa")
    except requests.exceptions.RequestException as e:
        print(f"ERRO: Falha ao completar a tarefa. Detalhes: {e}")
        return

    print(f"\n--- CICLO DO {AGENT_ID} CONCLUÍDO COM SUCESSO ---")

if __name__ == "__main__":
    run_agent()

