# sofia/backend/app/config_loader.py (Versão Corrigida)
import json
from pathlib import Path

def load_config():
    # Sobe dois níveis (de app/ -> backend/ -> sofia/) para encontrar a raiz
    project_root = Path(__file__).resolve().parent.parent.parent
    config_path = project_root / 'ecosystem_config.json'
    
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"--- ❌ ERRO CRÍTICO: Não foi possível carregar '{config_path}': {e} ---")
        return {}

config = load_config()

