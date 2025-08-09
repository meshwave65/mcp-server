# engine/stop.py
# VERSÃO: 2.0 - Implementa o backup seguro do .env

import os
import subprocess
from pathlib import Path

# --- LÓGICA DE BACKUP ---
# Define os caminhos de forma robusta
PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = PROJECT_ROOT / ".env"
BACKUP_DIR = PROJECT_ROOT / ".backup"
BACKUP_FILE = BACKUP_DIR / "env.bak"

def backup_env_file():
    """Copia o arquivo .env para um local de backup seguro."""
    if ENV_FILE.exists():
        print(f"--- 💾 [Backup] Encontrado arquivo .env. Criando backup seguro... ---")
        try:
            # Garante que o diretório de backup exista
            BACKUP_DIR.mkdir(exist_ok=True)
            # Copia o arquivo
            with open(ENV_FILE, 'r') as f_in, open(BACKUP_FILE, 'w') as f_out:
                f_out.write(f_in.read())
            print(f"✅ Backup do .env salvo em: {BACKUP_FILE}")
        except Exception as e:
            print(f"❌ Falha ao criar backup do .env: {e}")
    else:
        print("--- ⚠️ [Backup] Arquivo .env não encontrado. Nenhum backup foi criado. ---")

# --- LÓGICA DE ENCERRAMENTO (EXISTENTE) ---
def kill_processes():
    """Encerra os processos do ecossistema SOFIA."""
    print("\n--- 🛑 Iniciando o Encerramento de TODOS os Serviços do Ecossistema SOFIA 🛑 ---")
    # (A lógica para matar os processos do sentinel, uvicorn, vite, etc. permanece a mesma)
    # Exemplo simplificado:
    os.system("pkill -f 'sentinel.py' > /dev/null 2>&1")
    os.system("pkill -f 'uvicorn backend.main:app' > /dev/null 2>&1")
    os.system("pkill -f 'vite --host' > /dev/null 2>&1")
    print("✅ Processos do ecossistema encerrados.")

if __name__ == "__main__":
    backup_env_file()
    kill_processes()

