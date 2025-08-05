# sofia/backend/app/services/segments_service.py
from sqlalchemy.orm import Session, joinedload
from typing import List

# --- CORREÇÃO AQUI: Importação Explícita e Direta ---
# Importa a classe Segment diretamente do seu arquivo de definição.
from backend.app.models.segment import Segment

def get_all_segments_with_phases(db: Session) -> List[Segment]:
    """
    Busca todos os segmentos e carrega suas fases relacionadas (eager loading)
    para evitar múltiplas consultas ao banco de dados.
    """
    try:
        # Usa a classe Segment importada diretamente
        segments = db.query(Segment).options(joinedload(Segment.phases)).all()
        return segments
    except Exception as e:
        print(f"❌ ERRO CRÍTICO ao buscar segmentos no banco de dados: {e}")
        return []

