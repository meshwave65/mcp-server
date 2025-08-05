# sofia/backend/fsmw_module/app/fsmw_router.py
from flask import Blueprint, render_template
from .config_loader import config # O config_loader do FSMW

# Importa os blueprints específicos do FSMW
from .routes.main_routes import main_bp
from .routes.collections_routes import collections_bp

# Cria o Blueprint principal que representa todo o módulo FSMW
fsmw_bp = Blueprint('fsmw', __name__, template_folder='templates')

# Pega os prefixos de configuração de dentro do FSMW
fsmw_config = config.get('FSMW_CONFIG', {})
api_prefix = fsmw_config.get('API_BASE_PATH', '/api/v1')

# Registra as rotas de navegação e coleções DENTRO do blueprint principal do FSMW
fsmw_bp.register_blueprint(main_bp, url_prefix=api_prefix)
fsmw_bp.register_blueprint(collections_bp, url_prefix=f"{api_prefix}/collections")

# Rota principal do FSMW, que serve a sua interface
@fsmw_bp.route('/')
def index():
    # Passa a configuração para o template
    return render_template('index.html', app_config=config)

