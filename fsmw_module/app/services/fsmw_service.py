# sofia/fsmw_module/app/services/fsmw_service.py
from sqlalchemy.orm import Session
from pathlib import Path
from typing import Dict, List, Optional
import os

# Importa o carregador de configuração para obter o caminho raiz
from fsmw_module.app.config_loader import config as fsmw_config

def get_directory_content(db: Session, relative_path: str) -> Optional[Dict]:
    """
    Lista o conteúdo de um diretório no sistema de arquivos,
    respeitando a 'jaula' de segurança definida na configuração.
    """
    try:
        root_jail_str = fsmw_config.get("FSMW_CONFIG", {}).get("USER_ROOT_JAIL")
        if not root_jail_str:
            raise ValueError("USER_ROOT_JAIL não está definido na configuração.")

        root_jail = Path(root_jail_str).resolve()
        
        # Constrói o caminho alvo e resolve para um caminho absoluto
        # .lstrip('/') remove barras no início para evitar que Path o trate como absoluto
        target_path = (root_jail / relative_path.lstrip('/')).resolve()

        # --- Validação de Segurança Crucial ---
        # Garante que o caminho alvo ainda está DENTRO da jaula raiz
        if not str(target_path).startswith(str(root_jail)):
            print(f"⚠️ Acesso negado: Tentativa de acessar '{target_path}' fora da jaula '{root_jail}'")
            return None

        if not target_path.is_dir():
            return None

        subfolders = []
        files = []

        for entry in os.scandir(target_path):
            if entry.is_dir():
                subfolders.append({"name": entry.name})
            elif entry.is_file():
                stats = entry.stat()
                files.append({
                    "name": entry.name,
                    "size": stats.st_size,
                    "modified": stats.st_mtime
                })
        
        # Ordena alfabeticamente
        subfolders.sort(key=lambda x: x['name'].lower())
        files.sort(key=lambda x: x['name'].lower())

        # Retorna o caminho relativo à jaula
        display_path = '/' + str(target_path.relative_to(root_jail))
        if display_path == '/.': display_path = '/'


        return {
            "path": display_path,
            "subfolders": subfolders,
            "files": files
        }

    except Exception as e:
        print(f"❌ ERRO CRÍTICO no FSMW Service (get_directory_content): {e}")
        return None

# ... (outras funções de serviço podem ser implementadas depois) ...
def search_files_in_db(db: Session, search_term: str) -> List:
    return []

def get_file_path_by_id(db: Session, file_id: int) -> Optional[str]:
    return None

