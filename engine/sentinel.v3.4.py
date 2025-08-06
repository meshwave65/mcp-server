# sofia/engine/trinity_sentinel.py (v3.4 - Usando Script de Inicialização)

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

# --- Bloco de Configuração (sem alterações) ---
ENGINE_ROOT = Path(__file__).resolve().parent
BACKEND_DIR = ENGINE_ROOT / 'backend'
FRONTEND_DIR = ENGINE_ROOT / 'frontend'
BACKEND_PORT = 8000
FRONTEND_PORT = 5173
NGROK_API_URL = "http://localhost:4040/api/tunnels"
LOCAL_CONFIG_PATH = FRONTEND_DIR / 'public' / 'config.json'
FTP_CONFIG = {
    "host": "ftp.meshwave.com.br",
    "user": "meshwave1",
    "password": "Mesh#Wave#1965",
    "remote_path": "/public_html/sofia/config.json"
}

# --- Funções e Classe Sentinel (sem alterações até a definição do comando ) ---
# [Todo o código das funções e da classe Sentinel permanece o mesmo]
# ...
def get_ngrok_public_url() -> str | None:
    try:
        response = requests.get(NGROK_API_URL, timeout=5)
        response.raise_for_status()
        data = response.json()
        for tunnel in data.get("tunnels", []):
            if tunnel.get("proto") == "https" and "localhost" in tunnel.get("config", {}  ).get("addr"):
                return tunnel.get("public_url")
    except requests.exceptions.RequestException:
        return None
    return None

def update_config_files(new_url: str):
    print("--- Iniciando Sincronização do Arquivo de Configuração ---")
    config_content = {
        "backend_url": new_url,
        "last_updated_utc": datetime.now(timezone.utc).isoformat()
    }
    json_string = json.dumps(config_content, indent=2)
    try:
        LOCAL_CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(LOCAL_CONFIG_PATH, 'w') as f:
            f.write(json_string)
        print(f"✅ Arquivo local atualizado com sucesso em: {LOCAL_CONFIG_PATH}")
    except Exception as e:
        print(f"❌ ERRO ao escrever o arquivo de configuração local: {e}")
        return
    try:
        print(f"🔄 Conectando ao servidor FTP...")
        with FTP(timeout=15) as ftp:
            ftp.connect(FTP_CONFIG['host'])
            ftp.login(FTP_CONFIG['user'], FTP_CONFIG['password'])
            ftp.set_pasv(True)
            print("✅ Conexão FTP estabelecida.")
            json_bytes = io.BytesIO(json_string.encode('utf-8'))
            ftp.storbinary(f"STOR {FTP_CONFIG['remote_path']}", json_bytes)
            print(f"✅ Arquivo remoto atualizado com sucesso.")
    except Exception as e:
        print(f"❌ ERRO ao atualizar a configuração via FTP: {e}")

class Sentinel:
    def __init__(self):
        self.managed_pids = {"backend": None, "frontend": None, "ngrok": None}

    def get_pid_on_port(self, port):
        try:
            for conn in psutil.net_connections(kind='inet'):
                if conn.laddr.port == port and conn.status == psutil.CONN_LISTEN:
                    return conn.pid
        except Exception:
            return None
        return None

    def start_service(self, name, command, cwd):
        print(f"🔄 Iniciando o serviço '{name}' em '{cwd}'...")
        try:
            is_shell_needed = True if os.name == 'nt' and name == 'frontend' else False
            process = subprocess.Popen(command, cwd=cwd, shell=is_shell_needed)
            self.managed_pids[name] = process.pid
            print(f"✅ Serviço '{name}' iniciado com PID: {process.pid}")
            time.sleep(12)
        except Exception as e:
            print(f"❌ Falha catastrófica ao iniciar '{name}': {e}")

    def stop_service_by_pid(self, pid):
        if pid and psutil.pid_exists(pid):
            try:
                process = psutil.Process(pid)
                for child in process.children(recursive=True):
                    child.kill()
                process.kill()
                print(f"🔪 Processo e filhos (PID: {pid}) finalizados.")
            except psutil.NoSuchProcess:
                pass

    def check_and_manage_service(self, name, port, command, cwd):
        pid_on_port = self.get_pid_on_port(port)
        if pid_on_port and psutil.pid_exists(pid_on_port):
            return

        print(f"⚠️  Serviço '{name}' não está rodando. Tentando iniciar...")
        self.start_service(name, command, cwd)

    def run(self):
        print(f"--- 🛡️  Iniciando o Sentinela SOFIA (v3.4 - Usando Script de Inicialização) 🛡️ ---")
        
        # --- CORREÇÃO DEFINITIVA ---
        # O comando agora é simplesmente chamar o nosso script de inicialização.
        # O script cuidará de ativar o venv e executar o uvicorn.
        backend_cmd = ["./start_backend.sh"]
        
        npm_path = "npm"
        frontend_cmd = [npm_path, "run", "dev"]
        
        while True:
            print(f"\n--- Verificação às {time.strftime('%Y-%m-%d %H:%M:%S')} ---")
            
            self.check_and_manage_service("backend", BACKEND_PORT, backend_cmd, BACKEND_DIR)
            self.check_and_manage_service("frontend", FRONTEND_PORT, frontend_cmd, FRONTEND_DIR)

            if not self.get_pid_on_port(4040):
                 print("⚠️  Processo do Ngrok não encontrado. Tentando reiniciar...")
                 os.system("killall ngrok > /dev/null 2>&1")
                 time.sleep(2)
                 subprocess.Popen(f"ngrok http {BACKEND_PORT} > /dev/null 2>&1", shell=True )
                 time.sleep(5)

            ngrok_url = get_ngrok_public_url()
            if ngrok_url:
                print(f"✅ Túnel do Ngrok está ATIVO: {ngrok_url}")
                update_config_files(ngrok_url)
            else:
                print("❌ Falha ao obter a URL do Ngrok.")

            print("--- Verificação concluída. Próxima em 60 segundos. ---")
            time.sleep(60)

if __name__ == "__main__":
    print("--- Limpando processos antigos antes de iniciar... ---")
    os.system(f"kill -9 $(lsof -t -i:{BACKEND_PORT}) > /dev/null 2>&1")
    os.system(f"kill -9 $(lsof -t -i:{FRONTEND_PORT}) > /dev/null 2>&1")
    os.system("killall ngrok > /dev/null 2>&1")
    time.sleep(2)
    print("--- Limpeza concluída. Iniciando o Sentinela. ---")
    sentinel = Sentinel()
    sentinel.run()

