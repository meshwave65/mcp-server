# fsmw_project/indexer/indexer_service.py
import os
import time
from pathlib import Path
import mysql.connector
from datetime import datetime

# --- Configurações ---
# O usuário irá fornecer este caminho no futuro. Por enquanto, definimos um para teste.
# IMPORTANTE: Altere este caminho para a pasta que você deseja indexar!
# Linha 11
PATH_TO_INDEX = "/home/mesh/home/fsmw_project"  # Exemplo. Use um caminho real da sua máquina.

DB_CONFIG = {
    'user': 'root',
    'password': 'mesh1234',
    'host': '127.0.0.1',
    'port': 3306,
    'database': 'fsmw_db'
}

class Indexer:
    def __init__(self, root_path_to_index):
        self.root_path = Path(root_path_to_index).resolve()
        if not self.root_path.is_dir():
            raise ValueError(f"O caminho especificado não é um diretório válido: {self.root_path}")
        
        self.connection = mysql.connector.connect(**DB_CONFIG)
        self.cursor = self.connection.cursor(dictionary=True)
        print("✅ Conexão com o banco de dados estabelecida.")

    def _get_or_create_folder_id(self, folder_path: Path) -> int:
        """
        Verifica se uma pasta já existe no DB. Se não, a insere.
        Retorna o ID da pasta no banco de dados.
        """
        # Verifica se a pasta já está no DB
        self.cursor.execute("SELECT id FROM pastas WHERE caminho_completo = %s", (str(folder_path),))
        result = self.cursor.fetchone()
        if result:
            return result['id']

        # Se não existe, precisamos inseri-la. Primeiro, garantimos que o pai exista.
        parent_id = None
        if folder_path.parent != folder_path: # Evita recursão infinita na raiz
            parent_id = self._get_or_create_folder_id(folder_path.parent)

        # Insere a nova pasta
        sql = "INSERT INTO pastas (nome, caminho_completo, id_pai) VALUES (%s, %s, %s)"
        val = (folder_path.name, str(folder_path), parent_id)
        self.cursor.execute(sql, val)
        self.connection.commit()
        
        folder_id = self.cursor.lastrowid
        print(f"  [Pasta] Catalogada: {folder_path.name} (ID: {folder_id})")
        return folder_id

    def run_initial_scan(self):
        """
        Executa a varredura completa do diretório raiz e popula o banco de dados.
        """
        print(f"\n--- 🚀 Iniciando Varredura Inicial em: {self.root_path} 🚀 ---")
        start_time = time.time()
        file_count = 0
        folder_count = 0

        for dirpath, dirnames, filenames in os.walk(self.root_path):
            current_folder_path = Path(dirpath)
            
            # Garante que a pasta atual e todas as suas ancestrais estejam no DB
            folder_id = self._get_or_create_folder_id(current_folder_path)
            folder_count += 1

            for filename in filenames:
                file_path = current_folder_path / filename
                try:
                    stat = file_path.stat()
                    
                    # Verifica se o arquivo já foi indexado para evitar duplicatas
                    self.cursor.execute("SELECT id FROM arquivos WHERE caminho_completo = %s", (str(file_path),))
                    if self.cursor.fetchone():
                        continue # Pula para o próximo arquivo

                    # Insere o novo arquivo
                    sql = """
                        INSERT INTO arquivos 
                        (nome_arquivo, caminho_completo, tamanho_bytes, data_modificacao, id_pasta) 
                        VALUES (%s, %s, %s, %s, %s)
                    """
                    val = (
                        filename,
                        str(file_path),
                        stat.st_size,
                        datetime.fromtimestamp(stat.st_mtime),
                        folder_id
                    )
                    self.cursor.execute(sql, val)
                    self.connection.commit()
                    file_count += 1
                    print(f"    [Arquivo] Catalogado: {filename}")

                except (FileNotFoundError, PermissionError) as e:
                    print(f"    [Erro] Não foi possível acessar o arquivo {file_path}: {e}")
        
        end_time = time.time()
        print("\n--- ✅ Varredura Inicial Concluída! ---")
        print(f"  Pastas processadas: {folder_count}")
        print(f"  Novos arquivos catalogados: {file_count}")
        print(f"  Tempo total: {end_time - start_time:.2f} segundos")

    def close(self):
        """Fecha a conexão com o banco de dados."""
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("\n🔌 Conexão com o banco de dados fechada.")

if __name__ == "__main__":
    try:
        # IMPORTANTE: Certifique-se de que o caminho em PATH_TO_INDEX existe!
        indexer = Indexer(root_path_to_index=PATH_TO_INDEX)
        indexer.run_initial_scan()
        indexer.close()
    except ValueError as e:
        print(f"ERRO DE CONFIGURAÇÃO: {e}")
    except mysql.connector.Error as err:
        print(f"ERRO DE BANCO DE DADOS: {err}")


