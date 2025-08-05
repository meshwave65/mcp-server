# sofia/fsmw_module/app/routes/fsmw_router.py (Versão Restaurada e Autônoma)
from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pathlib import Path

# --- CORREÇÃO CRÍTICA AQUI ---
# Importa a conexão, o serviço E O SEU PRÓPRIO CONFIG_LOADER
from fsmw_module.app.database.session import get_fsmw_db
from fsmw_module.app.services import fsmw_service
from fsmw_module.app.config_loader import config as fsmw_config

router = APIRouter()

template_dir = Path(__file__).resolve().parent.parent / 'templates'
templates = Jinja2Templates(directory=str(template_dir))
print(f"--- ℹ️  [FSMW] Ponteiro de templates configurado para: {template_dir} ---")

@router.get("", include_in_schema=False)
async def redirect_to_fsmw_with_slash(request: Request):
    return RedirectResponse(url=f"{request.url.path}/", status_code=301)

@router.get("/", response_class=HTMLResponse)
async def fsmw_index(request: Request):
    """
    Serve a página principal, usando a configuração carregada pelo seu próprio módulo.
    """
    return templates.TemplateResponse("index.html", {"request": request, "app_config": fsmw_config})

# ... (o resto das rotas da API permanece o mesmo) ...
@router.get("/api/v1/browse")
def browse_path(path: str = "/", db: Session = Depends(get_fsmw_db)):
    content = fsmw_service.get_directory_content(db=db, relative_path=path)
    if content is None:
        raise HTTPException(status_code=404, detail="Caminho não encontrado ou acesso negado.")
    return content

@router.get("/api/v1/search")
def search_files(q: str, db: Session = Depends(get_fsmw_db)):
    results = fsmw_service.search_files_in_db(db=db, search_term=q)
    return results

@router.get("/api/v1/download/{file_id}")
def download_file(file_id: int, db: Session = Depends(get_fsmw_db)):
    file_path_str = fsmw_service.get_file_path_by_id(db=db, file_id=file_id)
    if not file_path_str:
        raise HTTPException(status_code=404, detail="Arquivo não encontrado.")
    file_path = Path(file_path_str)
    if not file_path.is_file():
        raise HTTPException(status_code=404, detail="Arquivo físico não encontrado no disco.")
    return FileResponse(path=file_path, filename=file_path.name, media_type='application/octet-stream')

