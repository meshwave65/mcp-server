# ~/home/sofia/engine/sentinel.py
# VERSÃO 8.2: Ajuste automático do --app-dir e log de depuração

import os
import time
import subprocess
import psutil
from pathlib import Path
from dotenv import dotenv_values

# --- Importa a configuração da arquitetura ---
from architecture import (
    ENGINE_ROOT,
    FRONTEND_DIR,
    VENV_PYTHON,
    ENV_FILE,
    BACKEND_PORT,
    FRONTEND_PORT
)

# Carrega as variáveis do .env.
env_vars = {
    **os.environ,
    **dotenv_values(ENV_FILE),
}

class Sentinel:
    def __init__(self, services_config):
        self.services = services_config

    def get_pid_on_port(self, port):
        try:
            for conn in psutil.net_connections(kind='inet'):
                if conn.laddr.port == port and conn.status == psutil.CONN_LISTEN:
                    return conn.pid
        except Exception:
            return None
        return None

    def start_service(self, service_key):
        config = self.services[service_key]
        name, command, cwd = config['name'], config['command'], config['cwd']

        print(f"\n[DEBUG] cwd: {cwd}")
        print(f"[DEBUG] comando: {' '.join(map(str, command))}")

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

    def ensure_vite_installed(self):
        package_json = FRONTEND_DIR / "package.json"
        node_modules_dir = FRONTEND_DIR / "node_modules"

        if not package_json.exists():
            print(f"❌ Não encontrei package.json em {FRONTEND_DIR}")
            return False

        if not node_modules_dir.exists() or not (FRONTEND_DIR / "node_modules" / "vite").exists():
            print("⚠️ Vite não encontrado. Instalando dependências do frontend...")
            subprocess.run(["npm", "install"], cwd=FRONTEND_DIR)
            subprocess.run(["npm", "install", "vite", "--save-dev"], cwd=FRONTEND_DIR)
            print("✅ Vite instalado.")
        else:
            print("✅ Vite já está instalado.")
        return True

    def run(self):
        print(f"--- 🛡️  Iniciando o Sentinela SOFIA (v8.2 - Ajuste Automático do --app-dir) 🛡️ ---")
        self.ensure_vite_installed()
        while True:
            print(f"\n--- Verificação às {time.strftime('%Y-%m-%d %H:%M:%S')} ---")
            for key in self.services.keys():
                self.check_and_manage_service(key)
            print("--- Verificação concluída. Próxima em 60 segundos. ---")
            time.sleep(60)

if __name__ == "__main__":
    # Calcula o caminho correto do diretório pai que contém 'backend'
    app_dir = ENGINE_ROOT
    if not (ENGINE_ROOT / "backend").exists():
        app_dir = ENGINE_ROOT.parent  # sobe um nível se não encontrar

    SERVICES = {
        "gateway": {
            "name": "Gateway de API Unificado",
            "port": BACKEND_PORT,
            "command": [
                str(VENV_PYTHON), "-m", "uvicorn", "backend.main:app",
                "--host", "0.0.0.0", "--port", str(BACKEND_PORT), "--reload",
                "--app-dir", str(app_dir)
            ],
            "cwd": app_dir
        },
        "frontend": {
            "name": "Interface Vite",
            "port": FRONTEND_PORT,
            "command": ["npm", "run", "dev", "--", "--host"],
            "cwd": FRONTEND_DIR
        }
    }

    sentinel = Sentinel(SERVICES)
    sentinel.run()

