# sofia/engine/backend/app/schemas/roadmap_schema.py

from pydantic import BaseModel
from typing import List

# Este modelo define a estrutura de um único módulo na resposta da API
class Module(BaseModel):
    id: int
    name: str
    status: str

    class Config:
        from_attributes = True

# Este modelo define a estrutura de uma fase, que contém uma lista de módulos
class Phase(BaseModel):
    phase_name: str
    modules: List[Module]

    class Config:
        from_attributes = True

# Este é o modelo principal que define um segmento, contendo uma lista de fases
class Segment(BaseModel):
    segment_name: str
    phases: List[Phase]

    class Config:
        from_attributes = True

