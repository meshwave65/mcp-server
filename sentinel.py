# ~/home/sofia/sentinel.py
# VERSÃO FINAL: Orquestrador 100% Python que gerencia TODOS os 3 serviços.

import os
import time
import subprocess
import psutil
from pathlib import Path
import sys
from dotenv import dotenv_values

# --- Configuração da Arquitetura ---
PROJECT_ROOT = Path(__file__).resolve().parent
VENV_PYTHON = PROJECT_ROOT / 'venv' / 'bin' / 'python'
BACKEND_DIR = PROJECT_ROOT / 'backend'
FRONTEND_DIR = PROJECT_ROOT / 'frontend'
FSMW_DIR = PROJECT_ROOT / 'fsmw_module'

# Carrega as variáveis do .env da raiz
env_vars = {**os.environ, **dotenv_values(PROJECT_ROOT / ".env")}

# --- INÍCIO DA CORREÇÃO CRÍTICA ---
# A configuração agora inclui os TRÊS serviços.
SERVICES = {
    "backend": {
        "name": "Backend SOFIA",
        "port": 8000,
        "command": [
            str(VENV_PYTHON), "-m", "uvicorn", "backend.main:app",
            "--host", "0.0.0.0", "--port", "8000", "--reload"
        ],
        "cwd": PROJECT_ROOT
    },
    "fsmw": {
        "name": "Módulo FSMW",
        "port": 8001,
        "command": [
            str(VENV_PYTHON), "-m", "uvicorn", "fsmw_module.main:app",
            "--host", "0.0.0.0", "--port", "8001", "--reload"
        ],
        "cwd": PROJECT_ROOT
    },
    "frontend": {
        "name": "Interface Vite",
        "port": 5173,
        "command": ["npm", "run", "dev", "--", "--host"],
        "cwd": FRONTEND_DIR
    }
}
# --- FIM DA CORREÇÃO CRÍTICA ---

# --- CLASSE SENTINEL E PONTO DE ENTRADA ---
# (O código da classe Sentinel e do if __name__ == "__main__" pode permanecer
# como na minha penúltima resposta, pois a lógica de gerenciamento está correta)
class Sentinel:
    def __init__(self, services_config):
        self.services = services_config

    def get_pid_on_port(self, port):
        try:
            for conn in psutil.net_connections(kind='inet'):
                if conn.laddr.port == port and conn.status == psutil.CONN_LISTEN:
                    return conn.pid
        except Exception: return None
        return None

    def start_service(self, service_key):
        config = self.services[service_key]
        name, command, cwd = config['name'], config['command'], config['cwd']
        print(f"🔄 Iniciando o serviço '{name}' em '{cwd}'...")
        try:
            subprocess.Popen(command, cwd=cwd, env=env_vars)
            print(f"✅ Serviço '{name}' iniciado.")
            time.sleep(12)
        except Exception as e:
            print(f"❌ Falha catastrófica ao iniciar '{name}': {e}")

    def check_and_manage_service(self, service_key):
        config = self.services[service_key]
        name, port = config['name'], config['port']
        if not self.get_pid_on_port(port):
            print(f"⚠️  Serviço '{name}' não está rodando. Tentando iniciar...")
            self.start_service(service_key)

    def run(self):
        print(f"--- 🛡️  Iniciando o Sentinela do Ecossistema SOFIA (Modo Python Puro) 🛡️ ---")
        while True:
            print(f"\n--- Verificação às {time.strftime('%Y-%m-%d %H:%M:%S')} ---")
            for key in self.services.keys():
                self.check_and_manage_service(key)
            # Adicione aqui a sua lógica de verificação e atualização do Ngrok
            print("--- Verificação concluída. Próxima em 60 segundos. ---")
            time.sleep(60)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--clean':
        subprocess.run(["python", "trinity_stop.py"])
        sys.exit(0)
    
    print("\n--- Iniciando o Sentinela... ---")
    sentinel = Sentinel(SERVICES)
    sentinel.run()

