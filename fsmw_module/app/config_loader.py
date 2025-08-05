# sofia/fsmw_module/app/config_loader.py
import json
from pathlib import Path

def load_config():
    try:
        # Sobe 3 níveis (de app/ -> fsmw_module/ -> sofia/) para encontrar a raiz
        project_root = Path(__file__).resolve().parent.parent.parent
        config_path = project_root / 'ecosystem_config.json'
        
        print(f"--- ℹ️  [FSMW] Tentando carregar configuração de: {config_path} ---")

        with open(config_path, 'r') as f:
            config_data = json.load(f)
            print("--- ✅ [FSMW] Configuração do ecossistema carregada com sucesso. ---")
            return config_data
            
    except Exception as e:
        raise RuntimeError(f"ERRO CRÍTICO no FSMW: Não foi possível carregar ou ler o arquivo de configuração: {e}")

config = load_config()

