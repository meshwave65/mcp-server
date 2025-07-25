import os
import subprocess
from fastapi import FastAPI, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel
import uvicorn

# --- Configuração de Segurança ---
# Em um ambiente real, este token viria de uma variável de ambiente ou um cofre de segredos.
# Para começar, vamos defini-lo aqui. Lembre-se de nunca commitar um token real.
API_TOKEN = "meshwave-secret-token-change-me" 
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

# --- Modelos de Dados (para validação de entrada) ---
class FileContent(BaseModel):
    path: str
    content: str

class Command(BaseModel):
    command: str
    
class PathRequest(BaseModel):
    path: str

# --- Inicialização do App FastAPI ---
app = FastAPI(
    title="MeshWave Model Context Protocol (MCP) Server",
    description="Uma ponte segura entre o agente Manus e o ambiente de desenvolvimento local.",
    version="0.1.0"
)

# --- Função de Dependência para Segurança ---
async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key == API_TOKEN:
        return api_key
    else:
        raise HTTPException(
            status_code=403,
            detail="Could not validate credentials",
        )

# --- Endpoints da API (As "Ferramentas" do Agente) ---

@app.post("/tools/list_files", dependencies=[Security(get_api_key)])
async def list_files(request: PathRequest):
    """Lista os arquivos e diretórios em um caminho especificado."""
    path = request.path
    if not os.path.exists(path) or not os.path.isdir(path):
        raise HTTPException(status_code=404, detail="Directory not found or is not a directory")
    try:
        files = os.listdir(path)
        return {"directory": path, "files": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tools/read_file", dependencies=[Security(get_api_key)])
async def read_file(request: PathRequest):
    """Lê o conteúdo de um arquivo especificado."""
    path = request.path
    if not os.path.exists(path) or not os.path.isfile(path):
        raise HTTPException(status_code=404, detail="File not found or is not a file")
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        return {"path": path, "content": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tools/write_file", dependencies=[Security(get_api_key)])
async def write_file(file_data: FileContent):
    """Escreve (ou sobrescreve) conteúdo em um arquivo especificado."""
    path = file_data.path
    try:
        # Garante que o diretório exista
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(file_data.content)
        return {"status": "success", "message": f"File '{path}' written successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tools/run_command", dependencies=[Security(get_api_key)])
async def run_command(cmd: Command):
    """Executa um comando de shell e retorna a saída."""
    try:
        # Usamos shell=True com cautela. Para nosso caso de uso controlado, é aceitável.
        # O split() ajuda a lidar com comandos com argumentos.
        result = subprocess.run(
            cmd.command.split(),
            capture_output=True,
            text=True,
            check=False # Não lança exceção se o comando falhar (retorno != 0)
        )
        return {
            "command": cmd.command,
            "return_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Ponto de Entrada para Execução ---
if __name__ == "__main__":
    # O servidor rodará em http://127.0.0.1:8000
    uvicorn.run(app, host="127.0.0.1", port=8000 )


