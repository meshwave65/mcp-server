# sofia/engine/backend/app/routers/roadmap_router.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

# Importações relativas dentro do projeto para maior clareza
from ..services import roadmap_service
from ..database import get_db
# CORREÇÃO: Importa os schemas do arquivo dedicado, em vez de defini-los aqui.
from ..schemas import roadmap_schema 

router = APIRouter(
    prefix="/api/v1/roadmap",
    tags=["Roadmap"]
)

# A anotação `response_model` agora usa o schema importado.
@router.get("/", response_model=List[roadmap_schema.Segment])
def read_roadmap(db: Session = Depends(get_db)):
    """
    Retorna a estrutura completa do roadmap do projeto,
    organizada por segmentos, fases e módulos.
    """
    full_roadmap = roadmap_service.get_full_roadmap(db)
    return full_roadmap

