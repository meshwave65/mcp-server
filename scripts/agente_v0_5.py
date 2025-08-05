# ~/home/sofia/agente_v0_5_1.py
# Versão final que usa o filtro de especialização para encontrar trabalho.

import requests
import time
import os
from pathlib import Path
from openai import OpenAI

# --- Configurações ---
AGENT_ID = "Agente-Ilustrador-v0.5.1"
# Este agente só se importa com tarefas de Geração de Imagem
MY_SPECIALIZATION_CODE = 1 
API_BASE_URL = "http://localhost:8000/api/v1"
IMAGE_STORAGE_PATH = Path.home( ) / "home/sofia/engine/backend/public/generated_images"

# --- Funções de Interação com a API SOFIA ---

def find_my_specialized_task():
    """Encontra a tarefa 'open' de maior prioridade para a MINHA especialização."""
    print(f"Procurando por tarefas com status 'open' e código de especialização '{MY_SPECIALIZATION_CODE}'...")
    try:
        # A chamada agora inclui o novo filtro agent_specialization_code
        url = f"{API_BASE_URL}/tasks?status=open&sort_by_priority=true&agent_specialization_code={MY_SPECIALIZATION_CODE}"
        response = requests.get(url)
        response.raise_for_status()
        tasks = response.json()
        return tasks[0] if tasks else None
    except requests.exceptions.RequestException as e:
        print(f"[ERRO] Falha ao buscar tarefas especializadas: {e}")
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

# --- Função de Lógica do Agente ---

def generate_image_from_prompt(prompt: str, task_id: str) -> str:
    """Usa a API da OpenAI para gerar uma imagem e a salva localmente."""
    print(f"  -> Conectando à API de Geração de Imagem...")
    try:
        # IMPORTANTE: Requer que a variável de ambiente OPENAI_API_KEY esteja configurada.
        client = OpenAI()
        response = client.images.generate(
            model="dall-e-3", prompt=prompt, size="1024x1024", quality="standard", n=1
        )
        image_url = response.data[0].url
        print(f"  -> Imagem gerada com sucesso. URL: {image_url}")
        
        image_data = requests.get(image_url).content
        file_name = f"{task_id}_result.png"
        local_path = IMAGE_STORAGE_PATH / file_name
        
        with open(local_path, "wb") as f:
            f.write(image_data)
        print(f"  -> Imagem salva em: {local_path}")
        return f"/public/generated_images/{file_name}"
    except Exception as e:
        print(f"  -> [ERRO DE GERAÇÃO] Falha ao gerar a imagem: {e}")
        return "/public/images/placeholder_error.png"

# --- Função Principal ---

def run_agent():
    print(f"--- INICIANDO {AGENT_ID} (Especialização: {MY_SPECIALIZATION_CODE}) ---")
    
    task = find_my_specialized_task()
    if not task:
        print("Nenhuma tarefa para minha especialização encontrada. Encerrando.")
        return
        
    task_id = task['id']
    print(f"Tarefa especializada encontrada: ID {task_id}")
    update_task_status(task_id, "in_progress", AGENT_ID)

    details = get_task_details(task_id)
    mission_prompt = next((b['content'] for b in details['blocks'] if b['sequence'] == 1), None)
    if not mission_prompt:
        print("ERRO: Bloco de descrição (prompt) não encontrado.")
        update_task_status(task_id, "on_hold")
        return
    print(f"Prompt para geração da imagem: '{mission_prompt[:80]}...'")

    print("Executando a missão de geração de imagem...")
    image_path = generate_image_from_prompt(mission_prompt, details.get('original_task_id', str(task_id)))

    report_content = (
        f"## Relatório de Geração de Artefato\n\n"
        f"A imagem solicitada foi gerada e armazenada com sucesso.\n\n"
        f"**Caminho do Artefato:** `{image_path}`"
    )
    add_block_to_task(task_id, AGENT_ID, "ArtifactGenerated", report_content)
    print("Relatório de artefato entregue com sucesso.")

    update_task_status(task_id, "done")
    print(f"--- CICLO DO {AGENT_ID} CONCLUÍDO ---")

if __name__ == "__main__":
    run_agent()

