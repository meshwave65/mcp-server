import json
import mysql.connector
import uuid
import re

# --- 1. DADOS DE ORIGEM (O JSON DA API) ---
json_data_string = """
[
  {
    "assigned_to": "IA-Agente-FILIPE",
    "created_at": "2025-07-31T03:33:07.451709+00:00",
    "due_date": null,
    "estimated_effort_hours": 8,
    "module_id": 1,
    "priority": 3,
    "project": "SOFIA-Core-Dev",
    "status_agente": 2,
    "tags": ["pesquisa", "arquitetura"],
    "task_id": "TSK-20250731-003",
    "title": "Análise Competitiva - Foco em Arquitetura",
    "turn_holder": 0,
    "updated_at": "2025-07-31T04:21:08.854118+00:00",
    "content": "# Análise Competitiva - Foco em Arquitetura\\n\\n## Descrição Inicial da Tarefa\\n> Realizar uma pesquisa aprofundada sobre os padrões de arquitetura (ex: microserviços, monolítico) de sistemas concorrentes ou similares ao SOFIA.\\n\\n---\\n### Bloco de Interação: 2025-07-31T03:33:07.451709+00:00 | Sistema\\n**Ação:** Tarefa Criada\\n**Mudança de Estado:** status_agente: 0 -> 1 | turn_holder: 0 -> 0\\n---\\n### Bloco de Interação: 2025-07-31T04:21:08.854118+00:00 | IA-Agente-FILIPE\\n**Ação:** Tarefa Atribuída\\n**Mudança de Estado:** status_agente: 1 -> 2 | assigned_to: any -> IA-Agente-FILIPE"
  },
  {
    "assigned_to": "IA-Agente-Luiz",
    "created_at": "2025-07-31T03:32:05.727029+00:00",
    "due_date": null,
    "estimated_effort_hours": 8,
    "module_id": 1,
    "priority": 3,
    "project": "SOFIA-Core-Dev",
    "status_agente": 2,
    "tags": ["pesquisa", "desempenho"],
    "task_id": "TSK-20250731-002",
    "title": "Análise Competitiva - Foco em Desempenho",
    "turn_holder": 0,
    "updated_at": "2025-07-31T04:43:08.498417+00:00",
    "content": "# Análise Competitiva - Foco em Desempenho\\n\\n## Descrição Inicial da Tarefa\\n> Realizar uma pesquisa aprofundada sobre o desempenho e a latência de sistemas concorrentes ou similares ao SOFIA.\\n\\n---\\n### Bloco de Interação: 2025-07-31T03:32:05.727029+00:00 | Sistema\\n**Ação:** Tarefa Criada\\n**Mudança de Estado:** status_agente: 0 -> 1 | turn_holder: 0 -> 0\\n---\\n### Bloco de Interação: 2025-07-31T04:43:08.498417+00:00 | IA-Agente-Luiz\\n**Ação:** Tarefa Atribuída\\n**Mudança de Estado:** status_agente: 1 -> 2 | assigned_to: any -> IA-Agente-Luiz"
  },
  {
    "assigned_to": "IA-Agente-NATALIA",
    "created_at": "2025-07-31T03:31:09.789450+00:00",
    "due_date": null,
    "estimated_effort_hours": 8,
    "module_id": 1,
    "priority": 2,
    "project": "SOFIA-Core-Dev",
    "status_agente": 2,
    "tags": ["pesquisa", "desempenho"],
    "task_id": "TSK-20250731-001",
    "title": "Análise Competitiva - Foco em Desempenho",
    "turn_holder": 0,
    "updated_at": "2025-07-31T05:03:26.796817+00:00",
    "content": "# Análise Competitiva - Foco em Desempenho\\n\\n## Descrição Inicial da Tarefa\\n> Realizar uma pesquisa aprofundada sobre o desempenho e a latência de sistemas concorrentes ou similares ao SOFIA.\\n\\n---\\n### Bloco de Interação: 2025-07-31T03:31:09.789450+00:00 | Sistema\\n**Ação:** Tarefa Criada\\n**Mudança de Estado:** status_agente: 0 -> 1 | turn_holder: 0 -> 0\\n---\\n### Bloco de Interação: 2025-07-31T05:03:26.796817+00:00 | IA-Agente-NATALIA\\n**Ação:** Tarefa Atribuída\\n**Mudança de Estado:** status_agente: 1 -> 2 | assigned_to: any -> IA-Agente-NATALIA"
  }
]
"""

# --- 2. CONFIGURAÇÕES E FUNÇÕES AUXILIARES ---

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root', # <-- VERIFIQUE E AJUSTE
    'password': 'mesh1234', # <-- VERIFIQUE E AJUSTE
    'database': 'meshwave_db'
}

def map_status(status_agente):
    """Converte o status numérico para o ENUM de texto."""
    if status_agente == 1:
        return 'open'
    if status_agente == 2:
        return 'in_progress'
    # Adicione outros mapeamentos se necessário
    return 'done'

def parse_content_to_blocks(content_string):
    """Analisa a string de conteúdo e a divide em blocos lógicos."""
    parts = re.split(r'\n---\n', content_string)
    blocks = []
    
    # Bloco 0 e 1 (Header e Briefing)
    header_and_briefing = parts[0].strip()
    match = re.search(r'(#.*?)\n\n(##.*)', header_and_briefing, re.DOTALL)
    if match:
        header_content = match.group(1).strip()
        briefing_content = match.group(2).strip()
        blocks.append({'type': 'Header', 'author': 'Sistema-Migrador', 'content': header_content})
        blocks.append({'type': 'DetailedDescription', 'author': 'Sistema-Migrador', 'content': briefing_content})
    else:
        # Fallback caso o padrão não seja encontrado
        blocks.append({'type': 'Header', 'author': 'Sistema-Migrador', 'content': header_and_briefing})

    # Blocos de Interação
    for interaction_part in parts[1:]:
        author_match = re.search(r'\|\s*([^\\n]+)', interaction_part)
        author = author_match.group(1).strip() if author_match else 'Desconhecido'
        blocks.append({'type': 'ProgressUpdate', 'author': author, 'content': interaction_part.strip()})
        
    return blocks

# --- 3. LÓGICA PRINCIPAL DA MIGRAÇÃO ---

def migrate():
    try:
        # Conecta ao banco de dados
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        print("Conexão com o banco de dados bem-sucedida.")

        # Carrega os dados do JSON
        tasks_data = json.loads(json_data_string)
        print(f"Encontradas {len(tasks_data)} tarefas no JSON para migrar.")

        for task in tasks_data:
            print(f"\nProcessando tarefa: {task['task_id']} - {task['title']}")

            # Insere na tabela `tasks`
            sql_insert_task = """
            INSERT INTO tasks (title, status, module_id, priority, assigned_to, original_task_id)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            task_values = (
                task['title'],
                map_status(task['status_agente']),
                task['module_id'],
                task['priority'],
                task['assigned_to'],
                task['task_id']
            )
            cursor.execute(sql_insert_task, task_values)
            new_task_id = cursor.lastrowid # Pega o ID auto-incrementado da nova tarefa
            print(f"  -> Tarefa inserida na tabela `tasks` com o novo ID: {new_task_id}")

            # Analisa o conteúdo e insere os blocos
            blocks = parse_content_to_blocks(task['content'])
            print(f"  -> Conteúdo analisado em {len(blocks)} blocos.")

            for i, block in enumerate(blocks):
                sql_insert_block = """
                INSERT INTO TaskBlocks (block_id, task_id, sequence, author_id, block_type, content)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                block_values = (
                    str(uuid.uuid4()),
                    new_task_id,
                    i, # Sequência 0, 1, 2...
                    block['author'],
                    block['type'],
                    block['content']
                )
                cursor.execute(sql_insert_block, block_values)
            
            print(f"  -> {len(blocks)} blocos inseridos na tabela `TaskBlocks`.")

        # Comita as transações
        conn.commit()
        print("\nMigração concluída com sucesso! Todas as alterações foram salvas.")

    except mysql.connector.Error as err:
        print(f"Erro de banco de dados: {err}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            print("Conexão com o banco de dados fechada.")

if __name__ == "__main__":
    migrate()

