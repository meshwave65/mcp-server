# sofia/backend/app/routes/roadmap_router.py (Refatorado)
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

# Importa o serviço correspondente e a dependência do DB
from backend.app.services import roadmap_service
from backend.app.database import get_db
from backend.app.schemas import roadmap_schema
from backend.app.database.session import get_db # CORRETO E CLARO

router = APIRouter(
    prefix="/api/v1/roadmap",
    tags=["Roadmap"]
)

@router.get("/", response_model=List[roadmap_schema.Segment])
def read_roadmap(db: Session = Depends(get_db)):
    """
    Retorna a estrutura completa do roadmap do projeto.
    A lógica agora está no serviço.
    """
    try:
        full_roadmap = roadmap_service.get_full_roadmap(db)
        return full_roadmap
    except Exception as e:
        # Se o serviço falhar, o roteador captura e retorna um erro HTTP claro.
        raise HTTPException(status_code=500, detail=f"Erro interno ao processar o roadmap: {e}")

