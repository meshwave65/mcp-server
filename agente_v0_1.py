import requests
import time

# Configurações da API baseadas na sua documentação
API_BASE_URL = "http://localhost:8000/api/v1"
# O ID da tarefa que você inseriu com sucesso no banco de dados
TASK_ID_TO_PROCESS = 2 

def run_agent_v0_1( ):
    """
    Executa o ciclo de vida completo para a tarefa de teste.
    """
    print("--- INICIANDO AGENTE SOFIA v0.1 ---")

    # 1. Buscar por tarefas abertas
    print(f"\n[PASSO 1] Procurando por tarefas com status 'open'...")
    try:
        response = requests.get(f"{API_BASE_URL}/tasks?status=open")
        response.raise_for_status() # Lança um erro para respostas 4xx/5xx
    except requests.exceptions.RequestException as e:
        print(f"ERRO: Não foi possível conectar à API. Verifique se o backend está rodando. Detalhes: {e}")
        return

    tasks = response.json()
    if not tasks:
        print("RESULTADO: Nenhuma tarefa 'open' encontrada.")
        return

    # Encontra nossa tarefa específica na lista
    target_task = next((task for task in tasks if task.get('id') == TASK_ID_TO_PROCESS), None)

    if not target_task:
        print(f"RESULTADO: A tarefa de teste com ID {TASK_ID_TO_PROCESS} não foi encontrada na lista de tarefas 'open'.")
        return
    
    print(f"RESULTADO: Tarefa de teste encontrada: ID {target_task['id']} - '{target_task['title']}'")

    # 2. Assumir a tarefa (mudar status para 'in_progress')
    print(f"\n[PASSO 2] Assumindo a tarefa {TASK_ID_TO_PROCESS}...")
    update_payload = {"status": "in_progress"}
    try:
        response = requests.patch(f"{API_BASE_URL}/tasks/{TASK_ID_TO_PROCESS}", json=update_payload)
        response.raise_for_status()
        print("RESULTADO: Tarefa assumida com sucesso. Status alterado para 'in_progress'.")
    except requests.exceptions.RequestException as e:
        print(f"ERRO: Falha ao assumir a tarefa. Detalhes: {e}")
        return

    # 3. Simular trabalho
    print("\n[PASSO 3] Executando o trabalho da tarefa (simulação de 5 segundos)...")
    time.sleep(5)
    print("RESULTADO: Trabalho simulado concluído.")

    # 4. Completar a tarefa (mudar status para 'done')
    print(f"\n[PASSO 4] Completando a tarefa {TASK_ID_TO_PROCESS}...")
    update_payload = {"status": "done"}
    try:
        response = requests.patch(f"{API_BASE_URL}/tasks/{TASK_ID_TO_PROCESS}", json=update_payload)
        response.raise_for_status()
        print("RESULTADO: Tarefa completada com sucesso! Status alterado para 'done'.")
    except requests.exceptions.RequestException as e:
        print(f"ERRO: Falha ao completar a tarefa. Detalhes: {e}")
        return

    print("\n--- CICLO DO AGENTE v0.1 CONCLUÍDO COM SUCESSO ---")

if __name__ == "__main__":
    run_agent_v0_1()

