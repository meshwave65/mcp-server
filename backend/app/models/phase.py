# sofia/backend/app/models/phase.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from backend.app.database.base import Base

class Phase(Base):
    __tablename__ = "phases"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    description = Column(String(1024))
    segment_id = Column(Integer, ForeignKey("segments.id"))

    # Define a relação inversa com o segmento
    segment = relationship("Segment", back_populates="phases")

