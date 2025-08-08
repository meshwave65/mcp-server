# engine/sentinel.py
# VERSÃO: 13.3 - Limpeza Agressiva de Porta (Anti-Zumbi)

import os
import time
import subprocess
import psutil
from pathlib import Path

# Importa as constantes do nosso ponto de verdade
from architecture import (
    ENGINE_ROOT,
    FRONTEND_DIR,
    VENV_PYTHON,
    BACKEND_PORT,
    FRONTEND_PORT
)

class Sentinel:
    def __init__(self, services_config):
        self.services = services_config

    def get_pid_on_port(self, port):
        """Verifica se há um processo escutando na porta especificada."""
        try:
            for conn in psutil.net_connections(kind='inet'):
                if conn.laddr.port == port and conn.status == psutil.CONN_LISTEN:
                    return conn.pid
        except psutil.AccessDenied:
            return -1
        except Exception:
            return None
        return None

    def force_kill_port(self, port):
        """
        Executa um comando de sistema para matar qualquer processo
        que esteja ocupando a porta especificada.
        """
        print(f"🧹 Limpeza Agressiva: Forçando o encerramento de qualquer processo na porta {port}...")
        # O comando 'lsof -t -i:PORT' lista o PID do processo na porta.
        # 'kill -9' força o encerramento desse PID.
        # '> /dev/null 2>&1' suprime a saída de erro se a porta já estiver livre.
        os.system(f"kill -9 $(lsof -t -i:{port}) > /dev/null 2>&1")
        time.sleep(1) # Dá um segundo para o sistema operacional liberar o socket.

    def start_service(self, service_key):
        """Inicia um serviço específico."""
        config = self.services[service_key]
        name, command, cwd = config['name'], config['command'], config['cwd']
        
        print(f"🔄 Iniciando o serviço '{name}' em '{cwd}'...")
        print(f"   Comando a ser executado: {' '.join(command)}")
        try:
            subprocess.Popen(command, cwd=cwd)
            print(f"✅ Comando para '{name}' enviado ao sistema.")
        except Exception as e:
            print(f"❌ FALHA CRÍTICA ao tentar iniciar '{name}': {e}")

    def check_and_manage_service(self, service_key):
        """Verifica o estado de um serviço e o gerencia."""
        config = self.services[service_key]
        port = config['port']
        name = config['name']

        pid = self.get_pid_on_port(port)

        if pid is None:
            print(f"⚠️  Porta {port} para o serviço '{name}' está DOWN.")
            # --- LÓGICA ANTI-ZUMBI ---
            self.force_kill_port(port)
            self.start_service(service_key)
        else:
            pass # Porta está UP, nenhuma ação necessária.

    def run(self):
        """O ciclo principal do Sentinela."""
        print(f"--- 🛡️  Sentinela SOFIA (v{VERSION}) 🛡️ ---")
        while True:
            print(f"\n--- Verificação às {time.strftime('%Y-%m-%d %H:%M:%S')} ---")
            for key in self.services.keys():
                self.check_and_manage_service(key)
            
            print("--- Verificação concluída. Próxima em 15 segundos. ---")
            time.sleep(15)

if __name__ == "__main__":
    VERSION = "13.3"

    # Limpa todas as portas do projeto ANTES de iniciar o ciclo
    print("--- Limpeza Inicial do Ambiente ---")
    os.system(f"kill -9 $(lsof -t -i:{BACKEND_PORT} -t -i:{FRONTEND_PORT}) > /dev/null 2>&1")
    time.sleep(1)

    # Definição dos serviços
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
    
    # Inicia o Sentinela
    sentinel = Sentinel(SERVICES)
    sentinel.run()

