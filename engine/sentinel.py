# engine/sentinel.py
# VERSÃO: 14.1 - Corrigindo a Ordem de Execução (Restore ANTES de Import)

import os
import time
import subprocess
import psutil
from pathlib import Path
import sys

# --- LÓGICA DE RESTAURAÇÃO (NO TOPO DO ARQUIVO) ---
# Define os caminhos de forma robusta
PROJECT_ROOT_SENTINEL = Path(__file__).resolve().parent.parent
ENV_FILE_SENTINEL = PROJECT_ROOT_SENTINEL / ".env"
BACKUP_DIR_SENTINEL = PROJECT_ROOT_SENTINEL / ".backup"
BACKUP_FILE_SENTINEL = BACKUP_DIR_SENTINEL / "env.bak"

def restore_env_if_missing():
    """Verifica se .env existe. Se não, tenta restaurar do backup."""
    if not ENV_FILE_SENTINEL.exists():
        print("--- ⚠️ [Restore] Arquivo .env não encontrado! ---")
        if BACKUP_FILE_SENTINEL.exists():
            print(f"--- 🔄 [Restore] Restaurando .env a partir do backup: {BACKUP_FILE_SENTINEL} ---")
            try:
                # Garante que o diretório de backup exista (caso de clone novo)
                BACKUP_DIR_SENTINEL.mkdir(exist_ok=True)
                with open(BACKUP_FILE_SENTINEL, 'r') as f_in, open(ENV_FILE_SENTINEL, 'w') as f_out:
                    f_out.write(f_in.read())
                print("✅ .env restaurado com sucesso.")
                # Retorna True para indicar que uma restauração ocorreu
                return True
            except Exception as e:
                print(f"❌ Falha crítica ao restaurar .env: {e}")
                sys.exit(1)
        else:
            print("❌ ERRO FATAL: .env não encontrado e nenhum arquivo de backup disponível.")
            print("   Por favor, crie um arquivo .env na raiz do projeto.")
            sys.exit(1)
    # Retorna False se nenhuma restauração foi necessária
    return False

# --- CÓDIGO PRINCIPAL DO SENTINEL ---
if __name__ == "__main__":
    # PASSO 1: Executa a verificação de restauração ANTES de qualquer outra coisa.
    restore_env_if_missing()

    # PASSO 2: AGORA, com a garantia de que .env existe, importa a arquitetura.
    # Esta importação agora será bem-sucedida.
    from architecture import (
        ENGINE_ROOT,
        FRONTEND_DIR,
        VENV_PYTHON,
        BACKEND_PORT,
        FRONTEND_PORT
    )

    # O resto do código do Sentinel permanece o mesmo
    class Sentinel:
        def __init__(self, services_config): self.services = services_config
        def get_pid_on_port(self, port):
            try:
                for conn in psutil.net_connections(kind='inet'):
                    if conn.laddr.port == port and conn.status == psutil.CONN_LISTEN: return conn.pid
            except: return None
        def start_service(self, service_key):
            config = self.services[service_key]
            name, command, cwd = config['name'], config['command'], config['cwd']
            print(f"🔄 Iniciando o serviço '{name}' em '{cwd}'...")
            print(f"   Comando: {' '.join(command)}")
            try: subprocess.Popen(command, cwd=cwd)
            except Exception as e: print(f"❌ Falha ao iniciar '{name}': {e}")
        def check_and_manage_service(self, service_key):
            if not self.get_pid_on_port(self.services[service_key]['port']): self.start_service(service_key)
        def run(self):
            print(f"--- 🛡️  Sentinela SOFIA (v14.1) 🛡️ ---")
            while True:
                for key in self.services.keys(): self.check_and_manage_service(key)
                time.sleep(15)

    # PASSO 3: Define os serviços e executa o Sentinel
    gateway_command = [
        str(VENV_PYTHON), "-m", "uvicorn", "backend.main:app",
        "--host", "0.0.0.0", "--port", str(BACKEND_PORT), "--reload"
    ]
    SERVICES = {
        "gateway": {
            "name": "Gateway de API Unificado", "port": BACKEND_PORT,
            "command": gateway_command, "cwd": str(ENGINE_ROOT)
        },
        "frontend": {
            "name": "Interface Vite", "port": FRONTEND_PORT,
            "command": ["npm", "run", "dev", "--", "--host"], "cwd": str(FRONTEND_DIR)
        }
    }

    os.system(f"kill -9 $(lsof -t -i:{BACKEND_PORT} -t -i:{FRONTEND_PORT}) > /dev/null 2>&1")
    time.sleep(1)
    Sentinel(SERVICES).run()

