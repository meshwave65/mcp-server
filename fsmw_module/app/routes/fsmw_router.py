# ~/home/sofia/fsmw_module/app/routes/fsmw_router.py
# VERSÃO FINAL: Define o prefixo e injeta a configuração no template.

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
import json

# --- Configuração dos Templates ---
templates_path = Path(__file__).resolve().parent.parent / "templates"
templates = Jinja2Templates(directory=str(templates_path))

# --- INÍCIO DA CORREÇÃO CRÍTICA ---
# Define o prefixo aqui. Todas as rotas neste arquivo serão relativas a /fsmw.
router = APIRouter(prefix="/fsmw", tags=["FSMW"])
# --- FIM DA CORREÇÃO CRÍTICA ---

@router.get("/", response_class=HTMLResponse)
async def read_fsmw_index(request: Request):
    """Serve a interface principal do FSMW (o arquivo index.html)."""
    app_config_data = {
        "api_urls": {
            "browse": "/fsmw/browse", # O caminho completo será /fsmw/browse
        }
    }
    context = {"request": request, "app_config": app_config_data}
    return templates.TemplateResponse("index.html", context)

@router.get("/browse")
def browse_directory(path: str = "/"):
    """API para listar o conteúdo de um diretório."""
    if ".." in path:
        raise HTTPException(status_code=400, detail="Caminho inválido.")
    return {
        "path": path,
        "subfolders": ["Pasta Exemplo 1", "Pasta Exemplo 2"],
        "files": ["arquivo_exemplo.txt", "outro_arquivo.md"]
    }

