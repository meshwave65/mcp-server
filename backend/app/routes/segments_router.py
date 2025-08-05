# sofia/backend/app/routes/segments_router.py (Refatorado)
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

# Importa o serviço correspondente e outras dependências
from backend.app.services import segments_service
from backend.app.schemas import roadmap_schema
from backend.app.database import get_db

router = APIRouter(
    prefix="/api/v1/segments",
    tags=["Segments"]
)

@router.get("/", response_model=List[roadmap_schema.Segment])
def read_segments(db: Session = Depends(get_db)):
    """
    Busca todos os segmentos e suas fases.
    A lógica agora está no serviço.
    """
    try:
        segments = segments_service.get_all_segments_with_phases(db)
        return segments
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno ao buscar segmentos: {e}")

