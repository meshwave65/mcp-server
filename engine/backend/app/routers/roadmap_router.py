# engine/backend/app/routers/roadmap_router.py
# VERSÃO: 1.3 - Sincronizado com a estrutura de DB correta

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

# --- CORREÇÃO CRÍTICA ---
# Importa a função de dependência 'get_sofia_db' do módulo correto 'connect_db.py'.
from ..database.connect_db import get_sofia_db

# Importa os schemas Pydantic que definem a estrutura da resposta.
from ..schemas import roadmap_schema

router = APIRouter(
    prefix="/api/v1/roadmap",
    tags=["Roadmap"]
)

@router.get("/", response_model=List[roadmap_schema.Segment])
def get_roadmap(db: Session = Depends(get_sofia_db)):
    """
    Retorna a estrutura completa do roadmap do projeto SOFIA.
    Este endpoint serve como um placeholder e retorna dados estáticos por enquanto.
    """
    # Dados estáticos para simular uma resposta do banco de dados.
    # No futuro, esta lógica será substituída por uma consulta real ao DB.
    mock_roadmap_data = [
        roadmap_schema.Segment(
            segment_name="Fase 1: Fundação e Estabilização",
            phases=[
                roadmap_schema.Phase(
                    phase_name="1.1 - Arquitetura de Dados",
                    modules=[
                        roadmap_schema.Module(id=1, name="Definição do Schema sofia_db", status="Completed"),
                        roadmap_schema.Module(id=2, name="Implementação dos Modelos SQLAlchemy", status="Completed")
                    ]
                ),
                roadmap_schema.Phase(
                    phase_name="1.2 - Estabilização do Backend",
                    modules=[
                        roadmap_schema.Module(id=3, name="Conexão com DB e Injeção de Dependência", status="In Progress"),
                        roadmap_schema.Module(id=4, name="Implementação dos Serviços de Tarefas", status="Pending")
                    ]
                )
            ]
        )
    ]
    return mock_roadmap_data

