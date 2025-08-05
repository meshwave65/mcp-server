# agente_v0_4.py (v4.1 - CORRIGIDO)
# Corrige o erro 422 ao calcular a sequência do novo bloco.

import requests
import uuid
from googlesearch import search

# --- Configurações ---
AGENT_ID = "Agente-Pesquisador-v0.4"
API_BASE_URL = "http://localhost:8000"

# --- Funções da Ferramenta ---
def perform_web_search(query: str, num_results: int = 5 ) -> str:
    """Realiza uma pesquisa na web e retorna um resumo formatado."""
    print(f"    -> Executando pesquisa externa com a query: '{query}'")
    try:
        results = search(query, num_results=num_results, lang="pt")
        
        report = f"# Relatório de Pesquisa: {query}\n\n"
        report += "## Resumo dos Resultados:\n\n"
        
        for i, result in enumerate(results):
            report += f"### Fonte {i+1}:\n"
            report += f"- **URL:** {result}\n\n"
            
        print("    RESULTADO: Pesquisa concluída e relatório gerado.")
        return report
    except Exception as e:
        print(f"    [ERRO] Falha na pesquisa externa: {e}")
        return f"# Erro na Pesquisa\n\nNão foi possível concluir a pesquisa devido a um erro: {e}"

# --- Lógica Principal do Agente ---
def run_agent():
    print(f"--- INICIANDO {AGENT_ID} ---")

    # [FASE 0] Obter e processar o Oráculo
    try:
        response = requests.get(f"{API_BASE_URL}/oracle")
        response.raise_for_status()
        print("[ORÁCULO] Manual de operações obtido com sucesso.")
        # Em um agente real, o conteúdo do Oráculo seria processado aqui.
    except requests.exceptions.RequestException as e:
        print(f"[ERRO] Não foi possível obter o Oráculo: {e}. Encerrando.")
        return

    # [FASE I] Seleção e Análise
    print("\n[FASE I] Buscando tarefa de maior prioridade...")
    try:
        response = requests.get(f"{API_BASE_URL}/api/v1/tasks?status=open&sort_by_priority=true")
        response.raise_for_status()
        tasks = response.json()

        if not tasks:
            print("RESULTADO: Nenhuma tarefa 'open' encontrada. Encerrando ciclo.")
            return

        task_to_process = tasks[0]
        task_id = task_to_process['id']
        print(f"RESULTADO: Tarefa selecionada. ID: {task_id}, Título: '{task_to_process['title']}', Prioridade: {task_to_process['priority']}")

        print(f"\n[FASE I] Assumindo a tarefa {task_id}...")
        update_payload = {"status": "in_progress", "assigned_to": AGENT_ID}
        response = requests.patch(f"{API_BASE_URL}/api/v1/tasks/{task_id}", json=update_payload)
        response.raise_for_status()
        print("RESULTADO: Tarefa assumida com sucesso.")

        print(f"\n[FASE I] Extraindo missão da tarefa {task_id}...")
        response = requests.get(f"{API_BASE_URL}/api/v1/tasks/{task_id}")
        response.raise_for_status()
        task_details = response.json()
        
        mission_block = next((block for block in task_details['blocks'] if block['sequence'] == 1 and block['block_type'] == 'DetailedDescription'), None)
        
        if not mission_block:
            print(f"[ERRO] Bloco de descrição da missão não encontrado para a tarefa {task_id}. Encerrando.")
            # Opcional: Mudar status da tarefa para 'on_hold'
            return
            
        mission_query = mission_block['content']
        print(f"RESULTADO: Missão extraída -> '{mission_query}'")

    except requests.exceptions.RequestException as e:
        print(f"[ERRO] Falha na Fase I: {e}. Encerrando.")
        return

    # [FASE II] Execução e Relatório
    print("\n[FASE II] Executando a missão de pesquisa...")
    report_content = perform_web_search(mission_query)

    print("\n[FASE II] Entregando o relatório como um novo bloco...")
    try:
        # --- INÍCIO DA CORREÇÃO ---
        # A forma mais segura de obter a próxima sequência é contar os blocos existentes.
        # A API já nos deu a lista de blocos em `task_details`.
        current_block_count = len(task_details.get('blocks', []))
        next_sequence = current_block_count 
        # Se já existem blocos 0 e 1, a contagem é 2. O próximo será o 2.
        # --- FIM DA CORREÇÃO ---

        block_payload = {
            "sequence": next_sequence,
            "block_type": "ArtifactGenerated",
            "author_id": AGENT_ID,
            "content": report_content
        }
        response = requests.post(f"{API_BASE_URL}/api/v1/tasks/{task_id}/blocks", json=block_payload)
        response.raise_for_status()
        print("RESULTADO: Novo bloco de relatório adicionado com sucesso.")

    except requests.exceptions.RequestException as e:
        print(f"[ERRO] Falha ao adicionar bloco à tarefa {task_id}: {e}")
        print(f"--- ENCERRANDO: Falha ao entregar o relatório para a tarefa {task_id}. ---")
        return

    # [FASE III] Conclusão
    print(f"\n[FASE III] Completando a tarefa {task_id}...")
    try:
        update_payload = {"status": "done"}
        response = requests.patch(f"{API_BASE_URL}/api/v1/tasks/{task_id}", json=update_payload)
        response.raise_for_status()
        print("RESULTADO: Tarefa completada com sucesso!")
    except requests.exceptions.RequestException as e:
        print(f"[ERRO] Falha ao completar a tarefa {task_id}: {e}")
        return

    print(f"\n--- CICLO DO {AGENT_ID} CONCLUÍDO COM SUCESSO ---")

if __name__ == "__main__":
    run_agent()

