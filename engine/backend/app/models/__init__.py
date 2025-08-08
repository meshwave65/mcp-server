# engine/backend/app/models/__init__.py
# VERSÃO: 1.1 - Sincronizado com o schema sofia_db v1.2

# Importa apenas as classes que REALMENTE existem no nosso novo models.py
from .models import Task, MetadataType, MetadataValue, TaskMetadata, TaskHistory

# Exporta essas classes para que outras partes da aplicação possam usá-las
__all__ = [
    "Task",
    "MetadataType",
    "MetadataValue",
    "TaskMetadata",
    "TaskHistory",
]

