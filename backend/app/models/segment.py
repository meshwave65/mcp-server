# sofia/backend/app/models/segment.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

# Importa a Base do nosso arquivo de banco de dados
from backend.app.database.base import Base

class Segment(Base):
    __tablename__ = "segments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True)
    description = Column(String(1024))

    # Define a relação com as fases
    phases = relationship("Phase", back_populates="segment")

