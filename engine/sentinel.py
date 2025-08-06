# ~/home/sofia/engine/sentinel.py (v3.5 - Final Integrado)

import os
import time
import json
import requests
import subprocess
import psutil
from pathlib import Path
from ftplib import FTP
import io
from datetime import datetime, timezone
from dotenv import dotenv_values

# --- Configuração da Arquitetura (a partir de 'engine') ---
ENGINE_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = ENGINE_ROOT.parent

# Caminhos para os módulos DENTRO de 'engine'
BACKEND_DIR = ENGINE_ROOT / 'backend'
FRONTEND_DIR = ENGINE_ROOT / 'frontend'
FSMW_DIR = ENGINE_ROOT / 'fsmw_module'

# Portas dos serviços
BACKEND_PORT = 8000
FRONTEND_PORT = 5173
FSMW_PORT = 8001
NGROK_API_URL = "http://localhost:4040/api/tunnels"

# Caminhos para o venv e .env na RAIZ do projeto
VENV_PYTHON = PROJECT_ROOT / 'venv' / 'bin' / 'python'
ENV_FILE = PROJECT_ROOT / '.env'

# Carrega as variáveis do .env da raiz
env_vars = {**os.environ, **dotenv_values(ENV_FILE )}

# ... (Suas funções get_ngrok_public_url e update_config_files permanecem aqui) ...

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
        print(f"--- 🛡️  Iniciando o Sentinela SOFIA (v3.5 - Integrado) 🛡️ ---")
        while True:
            print(f"\n--- Verificação às {time.strftime('%Y-%m-%d %H:%M:%S')} ---")
            for key in self.services.keys():
                self.check_and_manage_service(key)
            # ... (Sua lógica de Ngrok e FTP permanece aqui) ...
            print("--- Verificação concluída. Próxima em 60 segundos. ---")
            time.sleep(60)

if __name__ == "__main__":
    SERVICES = {
        "backend": {
            "name": "Backend SOFIA", "port": BACKEND_PORT,
            "command": [
                str(VENV_PYTHON), "-m", "uvicorn", "backend.main:app",
                "--host", "0.0.0.0", "--port", str(BACKEND_PORT), "--reload",
                "--app-dir", str(PROJECT_ROOT)
            ],
            "cwd": PROJECT_ROOT
        },
        "fsmw": {
            "name": "Módulo FSMW", "port": FSMW_PORT,
            "command": [
                str(VENV_PYTHON), "-m", "uvicorn", "fsmw_module.main:app",
                "--host", "0.0.0.0", "--port", str(FSMW_PORT), "--reload",
                "--app-dir", str(PROJECT_ROOT)
            ],
            "cwd": PROJECT_ROOT
        },
        "frontend": {
            "name": "Interface Vite", "port": FRONTEND_PORT,
            "command": ["npm", "run", "dev", "--", "--host"],
            "cwd": FRONTEND_DIR
        }
    }

    # ... (Sua lógica de limpeza de processos antigos) ...
    print("--- Limpeza concluída. Iniciando o Sentinela. ---")
    
    sentinel = Sentinel(SERVICES)
    sentinel.run()

