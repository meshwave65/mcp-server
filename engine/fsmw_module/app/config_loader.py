# sofia/fsmw_module/app/config_loader.py
import json
import os
from pathlib import Path

def load_config():
    """
    Carrega o arquivo de configuração do ecossistema de forma robusta.
    """
    try:
        # 1. Obtém o caminho absoluto do diretório deste arquivo (config_loader.py)
        # Ex: /home/mesh/home/sofia/fsmw_module/app
        current_dir = Path(__file__).resolve().parent
        
        # 2. Sobe DOIS níveis para chegar à raiz do projeto SOFIA
        # Ex: /home/mesh/home/sofia
        project_root = current_dir.parent.parent
        
        # 3. Constrói o caminho completo e seguro para o arquivo de configuração
        config_path = project_root / 'ecosystem_config.json'
        
        print(f"--- ℹ️  [FSMW] Tentando carregar configuração de: {config_path} ---")

        with open(config_path, 'r') as f:
            config_data = json.load(f)
            print("--- ✅ [FSMW] Configuração do ecossistema carregada com sucesso. ---")
            return config_data
            
    except FileNotFoundError:
        raise RuntimeError(f"ERRO CRÍTICO: O arquivo de configuração não foi encontrado em '{config_path}'.")
    except json.JSONDecodeError:
        raise RuntimeError(f"ERRO CRÍTICO: O arquivo '{config_path}' contém um erro de sintaxe JSON.")

# Carrega a configuração uma vez quando o módulo é importado
config = load_config()

