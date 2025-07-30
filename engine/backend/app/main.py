# =============================================================================
# ARQUIVO COMPLETO: sofia/engine/backend/app/main.py
# VERSÃO: 2.4 - Lógica de Status Inteligente (Frontend prova que está vivo)
# =============================================================================

# --- BLOCO DE IMPORTAÇÕES ---
import json
import os
import socket
from pathlib import Path
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import requests

from . import database
from .models import models

# =============================================================================
# BLOCO 1: INICIALIZAÇÃO DO BANCO DE DADOS
# =============================================================================
try:
    print("INFO: Verificando e criando tabelas no banco de dados...")
    models.Base.metadata.create_all(bind=database.engine)
    print("INFO: Comando create_all do banco de dados executado com sucesso.")
except Exception as e:
    print(f"ERRO CRÍTICO: Ocorreu um erro ao criar as tabelas do banco de dados: {e}")

# =============================================================================
# BLOCO 2: APLICAÇÃO FASTAPI E MIDDLEWARE
# =============================================================================

app = FastAPI(title="Motor SOFIA API")

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
 )

# =============================================================================
# BLOCO 3: LÓGICA DE CONFIGURAÇÃO E ENDPOINTS
# =============================================================================

SOFIA_ROOT_PATH = Path(__file__).resolve().parents[3]
CURRENT_CLIENT = "meshwave"

class ProjectManager:
    # ... (A classe ProjectManager permanece exatamente a mesma) ...
    def __init__(self, sofia_root: Path, client_name: str):
        self.client_config_path = sofia_root / 'clients' / client_name / 'config_sofia.json'
        self.config = self._load_config()
    def _load_config(self) -> dict:
        try:
            with open(self.client_config_path, 'r') as f:
                print(f"INFO: Carregando configuração de projetos de: {self.client_config_path}")
                return json.load(f)
        except FileNotFoundError:
            print(f"ERRO CRÍTICO: Arquivo de configuração de projetos não encontrado em {self.client_config_path}")
            return {"projects": {}}
        except json.JSONDecodeError:
            print(f"ERRO CRÍTICO: O arquivo de configuração {self.client_config_path} contém um JSON inválido.")
            return {"projects": {}}
    def get_all_project_names(self) -> list:
        return list(self.config.get("projects", {}).keys())
    def get_project_path(self, project_name: str) -> Path:
        try:
            project_path_str = self.config["projects"][project_name]["path"]
            project_path = Path(project_path_str)
            if not project_path.is_dir():
                 raise HTTPException(status_code=500, detail=f"Config Error: O caminho para '{project_name}' não existe: {project_path}")
            return project_path
        except KeyError:
            raise HTTPException(status_code=404, detail=f"Projeto '{project_name}' não encontrado no arquivo de configuração.")

manager = ProjectManager(SOFIA_ROOT_PATH, CURRENT_CLIENT)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ... (Endpoints / e /projects permanecem os mesmos) ...
@app.get("/")
def read_root():
    return {"message": "Bem-vindo ao motor SOFIA!", "cliente_ativo": CURRENT_CLIENT}

@app.get("/projects")
def list_projects():
    project_names = manager.get_all_project_names()
    return {"client": CURRENT_CLIENT, "projects": project_names}

# ... (Endpoints de tasks, segments e phases permanecem os mesmos) ...
@app.get("/projects/{project_name}/tasks")
def list_tasks_for_project(project_name: str):
    project_path = manager.get_project_path(project_name)
    tasks_path = project_path / 'tasks'
    if not tasks_path.is_dir():
        return {"project": project_name, "tasks": []}
    try:
        task_files = [f.name for f in tasks_path.glob('*.py') if f.name != '__init__.py']
        return {"project": project_name, "tasks_path": str(tasks_path), "tasks": task_files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao ler o diretório de tarefas: {e}")

@app.get("/api/v1/segments")
def read_segments(db: Session = Depends(get_db)):
    segments = db.query(models.Segment).order_by(models.Segment.id).all()
    return segments

@app.get("/api/v1/segments/{segment_id}/phases")
def read_phases_for_segment(segment_id: int, db: Session = Depends(get_db)):
    segment = db.query(models.Segment).filter(models.Segment.id == segment_id).first()
    if not segment:
        raise HTTPException(status_code=404, detail="Segmento não encontrado")
    phases = db.query(models.Phase).filter(models.Phase.segment_id == segment_id).order_by(models.Phase.order).all()
    return phases

# =============================================================================
# BLOCO 4: ENDPOINTS DE DIAGNÓSTICO DO MOTOR (COM LÓGICA CORRIGIDA)
# =============================================================================

NGROK_API_PORT = 4040
BACKEND_PORT = 8000

def check_local_service(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        return s.connect_ex(('localhost', port)) == 0

@app.get("/api/v1/engine/status")
def get_engine_status():
    # --- A CORREÇÃO ESTÁ AQUI ---
    # A lógica para o frontend foi simplificada.
    # Se esta função está sendo chamada, é porque o frontend está, por definição,
    # ativo e se comunicando.
    status_report = {
        "backend": {"status": "ATIVO", "detail": f"Respondendo na porta {BACKEND_PORT}"},
        "frontend": {"status": "ATIVO", "detail": "Comunicação estabelecida com o Backend."},
        "ngrok": {"status": "PARADO", "url": None, "detail": "API do NGROK não encontrada."}
    }
    # --- FIM DA CORREÇÃO ---

    # A verificação do NGROK continua a mesma
    if check_local_service(NGROK_API_PORT):
        try:
            response = requests.get(f"http://localhost:{NGROK_API_PORT}/api/tunnels", timeout=2 )
            if response.status_code == 200:
                tunnels = response.json().get("tunnels", [])
                for tunnel in tunnels:
                    if tunnel.get("proto") == "https":
                        status_report["ngrok"]["status"] = "ATIVO"
                        status_report["ngrok"]["url"] = tunnel.get("public_url" )
                        status_report["ngrok"]["detail"] = f"Túnel para http://localhost:{BACKEND_PORT}"
                        break
        except requests.RequestException as e:
            status_report["ngrok"]["detail"] = f"API do NGROK encontrada, mas houve um erro: {e}"
            pass
    return status_report

