# sofia/engine/trinity_sentinel.py (v2.1 - Correção do CWD do Backend)

import os
import time
import json
import requests
import subprocess
from pathlib import Path

# =============================================================================
# BLOCO 1: CONFIGURAÇÃO BASEADA NA ARQUITETURA SOFIA
# =============================================================================
ENGINE_ROOT = Path(__file__).resolve().parent
SOFIA_ROOT = ENGINE_ROOT.parent
BACKEND_DIR = ENGINE_ROOT / 'backend'
FRONTEND_DIR = ENGINE_ROOT / 'frontend'
CLIENT_NAME = "meshwave"
CONFIG_FILE_PATH = SOFIA_ROOT / 'clients' / CLIENT_NAME / 'config_sofia.json'
BACKEND_PORT = 8000
FRONTEND_PORT = 5173
NGROK_API_URL = "http://localhost:4040/api/tunnels"

# =============================================================================
# BLOCO 2: FUNÇÕES DE SERVIÇO ADAPTADAS
# =============================================================================

def check_service(name: str, port: int ) -> bool:
    try:
        requests.get(f"http://localhost:{port}", timeout=5 )
        return True
    except requests.exceptions.ConnectionError:
        print(f"⚠️  Serviço '{name}' está INATIVO na porta {port}.")
        return False

def start_backend():
    """Inicia o servidor de Backend usando o venv correto."""
    print("🔄 Iniciando o servidor de Backend (Uvicorn)...")
    venv_python = BACKEND_DIR / 'venv' / 'bin' / 'python'
    command = [
        str(venv_python),
        "-m", "uvicorn",
        "app.main:app",
        "--host", "localhost",
        "--port", str(BACKEND_PORT)
    ]
    # --- A CORREÇÃO ESTÁ AQUI ---
    # O diretório de trabalho (cwd) deve ser o BACKEND_DIR, para que ele possa encontrar o módulo 'app'.
    subprocess.Popen(command, cwd=BACKEND_DIR)
    # --- FIM DA CORREÇÃO ---
    time.sleep(10)

def start_frontend():
    """Inicia o servidor de desenvolvimento do Frontend."""
    print("🔄 Iniciando o servidor de Frontend (NPM)...")
    command = ["npm", "run", "dev"]
    subprocess.Popen(command, cwd=FRONTEND_DIR)
    time.sleep(15)

def get_ngrok_public_url() -> str | None:
    """Obtém a URL pública do túnel NGROK que aponta para o nosso backend."""
    try:
        response = requests.get(NGROK_API_URL, timeout=5)
        response.raise_for_status()
        data = response.json()
        for tunnel in data.get("tunnels", []):
            if tunnel.get("proto") == "https" and tunnel.get("config", {} ).get("addr") == f"http://localhost:{BACKEND_PORT}":
                return tunnel.get("public_url" )
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        print(f"DEBUG: Não foi possível conectar à API do NGROK: {e}")
        return None
    return None

def start_ngrok():
    """Inicia um novo túnel do Ngrok em background."""
    print("🔄 Iniciando um novo túnel do Ngrok...")
    command = ["ngrok", "http", str(BACKEND_PORT ), "--log=stdout", ">", "/dev/null"]
    subprocess.Popen(" ".join(command), shell=True)
    time.sleep(10)

def update_local_config(project_name: str, new_url: str):
    """Atualiza o arquivo config_sofia.json localmente."""
    print(f"🔄 Atualizando '{CONFIG_FILE_PATH}' com a nova URL: {new_url}")
    try:
        with open(CONFIG_FILE_PATH, 'r') as f:
            config_data = json.load(f)
        if config_data.get("projects", {}).get(project_name, {}).get("ngrok_url") == new_url:
            print("✅ URL no config_sofia.json já está correta.")
            return
        config_data["projects"][project_name]["ngrok_url"] = new_url
        with open(CONFIG_FILE_PATH, 'w') as f:
            json.dump(config_data, f, indent=2)
        print("✅ Arquivo config_sofia.json atualizado localmente.")
    except (FileNotFoundError, KeyError, json.JSONDecodeError) as e:
        print(f"❌ ERRO ao atualizar o config_sofia.json: {e}")

# =============================================================================
# BLOCO 3: LOOP PRINCIPAL DO SENTINELA
# =============================================================================
if __name__ == "__main__":
    print("--- 🛡️  Iniciando o Sentinela SOFIA (v2.1 - Corrigido) 🛡️ ---")
    TARGET_PROJECT = "project_AppMWC"
    while True:
        print(f"\n--- Verificação às {time.strftime('%Y-%m-%d %H:%M:%S')} ---")
        if not check_service("Backend", BACKEND_PORT):
            start_backend()
        if not check_service("Frontend", FRONTEND_PORT):
            start_frontend()
        ngrok_url = get_ngrok_public_url()
        if not ngrok_url:
            print("⚠️  Túnel do Ngrok está INATIVO.")
            start_ngrok()
            time.sleep(5)
            ngrok_url = get_ngrok_public_url()
        if ngrok_url:
            print(f"✅ Túnel do Ngrok está ATIVO: {ngrok_url}")
            update_local_config(TARGET_PROJECT, ngrok_url)
        else:
            print("❌ Falha ao estabelecer o túnel do Ngrok após tentativa.")
        print("--- Verificação concluída. Próxima em 60 segundos. ---")
        time.sleep(60)

