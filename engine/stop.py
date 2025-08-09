# engine/stop.py
# VERSÃO: 2.1 - Usando .bkp para o backup real

import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = PROJECT_ROOT / ".env"
BACKUP_DIR = PROJECT_ROOT / ".backup"
# --- MUDANÇA CRÍTICA ---
BACKUP_FILE = BACKUP_DIR / "env.bkp" # Agora salva como .bkp

def backup_env_file():
    if ENV_FILE.exists():
        print(f"--- 💾 [Backup] Criando backup seguro em {BACKUP_FILE} ---")
        try:
            BACKUP_DIR.mkdir(exist_ok=True)
            with open(ENV_FILE, 'r') as f_in, open(BACKUP_FILE, 'w') as f_out:
                f_out.write(f_in.read())
            print("✅ Backup do .env salvo com sucesso.")
        except Exception as e:
            print(f"❌ Falha ao criar backup do .env: {e}")
    else:
        print("--- ⚠️ [Backup] Arquivo .env não encontrado. Nenhum backup foi criado. ---")

def kill_processes():
    print("\n--- 🛑 Encerrando serviços do ecossistema SOFIA... ---")
    os.system("pkill -f 'sentinel.py' > /dev/null 2>&1")
    os.system("pkill -f 'uvicorn backend.main:app' > /dev/null 2>&1")
    os.system("pkill -f 'vite --host' > /dev/null 2>&1")
    print("✅ Processos encerrados.")

if __name__ == "__main__":
    backup_env_file()
    kill_processes()

