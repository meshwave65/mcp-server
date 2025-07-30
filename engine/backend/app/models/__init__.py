# Importa apenas as classes que REALMENTE existem no arquivo models.py
# para que possam ser facilmente acessadas por outras partes da aplicação se necessário.
from .models import Module, MetadataType, MetadataValue, ModuleMetadata

# A importação do Base não é estritamente necessária aqui, mas não causa problemas.
# Vamos removê-la para manter o arquivo o mais limpo possível.

