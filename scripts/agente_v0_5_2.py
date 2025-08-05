# ~/home/sofia/agente_v0_5_2.py
# Versão SIMPLIFICADA para testar o ciclo completo sem filtros complexos.
# Ele pegará a PRIMEIRA tarefa 'open' que encontrar.

import requests
import time
import os
from pathlib import Path
# Supondo que a biblioteca openai esteja instalada
# from openai import OpenAI 

# --- Configurações ---
AGENT_ID = "Agente-Tester-v0.5.2"
API_BASE_URL = "http://localhost:8000/api/v1"
IMAGE_STORAGE_PATH = Path.home( ) / "home/sofia/engine/backend/public/generated_images"

# --- Funções de Interação com a API SOFIA ---

def find_first_open_task():
    """Encontra a primeira tarefa 'open' disponível, sem filtros extras."""
    print("Procurando pela primeira tarefa com status 'open'...")
    try:
        # --- MUDANÇA PRINCIPAL: URL SIMPLIFICADA ---
        url = f"{API_BASE_URL}/tasks?status=open"
        response = requests.get(url)
        response.raise_for_status()
        tasks = response.json()
        return tasks[0] if tasks else None
    except requests.exceptions.RequestException as e:
        print(f"[ERRO] Falha ao buscar tarefas: {e}")
        return None

def get_task_details(task_id):
    response = requests.get(f"{API_BASE_URL}/tasks/{task_id}")
    response.raise_for_status()
    return response.json()

def update_task_status(task_id, status, assigned_to=None):
    payload = {"status": status}
    if assigned_to: payload["assigned_to"] = assigned_to
    response = requests.patch(f"{API_BASE_URL}/tasks/{task_id}", json=payload)
    response.raise_for_status()
    return response.json()

def add_block_to_task(task_id, author_id, block_type, content):
    details = get_task_details(task_id)
    next_sequence = len(details.get('blocks', []))
    payload = {"author_id": author_id, "block_type": block_type, "content": content, "sequence": next_sequence}
    response = requests.post(f"{API_BASE_URL}/tasks/{task_id}/blocks", json=payload)
    response.raise_for_status()
    return response.json()

# --- Função de Lógica do Agente (Simulada) ---

def process_task_content(mission_prompt: str, task_id: str) -> str:
    """
    Simula o processamento da tarefa. Em um agente real, aqui ocorreria
    a pesquisa na web ou a geração de imagem.
    """
    print(f"  -> Processando a missão: '{mission_prompt[:80]}...'")
    time.sleep(5) # Simula 5 segundos de trabalho
    
    # Cria um relatório de simulação
    report = (
        f"## Relatório de Execução da Tarefa (Simulação)\n\n"
        f"A missão foi processada com sucesso pelo {AGENT_ID}.\n\n"
        f"**Missão Recebida:**\n> {mission_prompt}\n\n"
        f"**Resultado:**\nO trabalho foi concluído com base na missão fornecida."
    )
    print("  -> Simulação de trabalho concluída e relatório gerado.")
    return report

# --- Função Principal ---

def run_agent():
    print(f"--- INICIANDO {AGENT_ID} (Modo Simplificado) ---")
    
    task = find_first_open_task()
    if not task:
        print("Nenhuma tarefa 'open' encontrada. Encerrando.")
        return
        
    task_id = task['id']
    print(f"Tarefa encontrada: ID {task_id}")
    update_task_status(task_id, "in_progress", AGENT_ID)

    details = get_task_details(task_id)
    # Tenta encontrar um bloco de descrição, mas não falha se não encontrar.
    mission_prompt = "Nenhuma descrição detalhada encontrada. Executando com base no título."
    if details.get('blocks'):
        mission_block = next((b['content'] for b in details['blocks'] if b['sequence'] == 1), None)
        if mission_block:
            mission_prompt = mission_block

    print(f"Iniciando processamento da tarefa...")
    report_content = process_task_content(mission_prompt, str(task_id))

    add_block_to_task(task_id, AGENT_ID, "ArtifactGenerated", report_content)
    print("Relatório de execução entregue com sucesso.")

    update_task_status(task_id, "done")
    print(f"--- CICLO DO {AGENT_ID} CONCLUÍDO ---")

if __name__ == "__main__":
    run_agent()

