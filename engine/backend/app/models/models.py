# sofia/engine/backend/app/models/models.py (VERSÃO FINAL CORRIGIDA)

from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func

# --- CORREÇÃO PRINCIPAL ---
# A importação original era ".database", que procura o arquivo na pasta atual (models/).
# A importação correta é "..database", que diz ao Python para "voltar um diretório"
# (de app/models/ para app/) e então encontrar o arquivo database.py.
from ..database import Base

# Representa a tabela 'modules'
class Module(Base):
    __tablename__ = "modules"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String, default='Planejado')
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

# Representa a tabela 'metadata_types'
class MetadataType(Base):
    __tablename__ = "metadata_types"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

# Representa a tabela 'metadata_values'
class MetadataValue(Base):
    __tablename__ = "metadata_values"
    id = Column(Integer, primary_key=True, index=True)
    type_id = Column(Integer, ForeignKey("metadata_types.id"), nullable=False)
    value = Column(String, nullable=False)

# Representa a tabela de junção 'module_metadata'
class ModuleMetadata(Base):
    __tablename__ = "module_metadata"
    module_id = Column(Integer, ForeignKey("modules.id"), primary_key=True)
    metadata_value_id = Column(Integer, ForeignKey("metadata_values.id"), primary_key=True)

