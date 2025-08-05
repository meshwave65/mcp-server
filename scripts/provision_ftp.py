# fsmw_project/provision_ftp.py (Versão 2.0 - Leitura Manual)
import os
from ftplib import FTP, error_perm
import io
from pathlib import Path

# --- NOSSA PRÓPRIA FUNÇÃO PARA LER O .ENV ---
def load_manual_env():
    """
    Lê manualmente um arquivo .env e carrega as variáveis no ambiente.
    Isso evita problemas com a biblioteca python-dotenv.
    """
    # Constrói o caminho para o arquivo .env que está ao lado deste script
    script_dir = Path(__file__).resolve().parent
    dotenv_path = script_dir / '.env'
    print(f"--- ℹ️  Lendo .env manualmente de: {dotenv_path} ---")
    
    try:
        with open(dotenv_path) as f:
            for line in f:
                # Ignora linhas em branco e comentários
                if line.strip() and not line.strip().startswith('#'):
                    key, value = line.strip().split('=', 1)
                    # Define a variável de ambiente para este processo
                    os.environ[key.strip()] = value.strip()
        print("--- ✅ Variáveis do .env carregadas manualmente. ---")
    except FileNotFoundError:
        print(f"❌ ERRO CRÍTICO: Arquivo .env não encontrado em {dotenv_path}")
    except Exception as e:
        print(f"❌ ERRO ao ler o arquivo .env: {e}")

# Executa nossa função manual imediatamente
load_manual_env()

# O resto do script agora usa os.getenv() como antes, mas com as variáveis
# que nós mesmos carregamos.
FTP_CONFIG = {
    "host": os.getenv("FTP_HOST"),
    "user": os.getenv("FTP_USER"),
    "password": os.getenv("FTP_PASSWORD"),
    "base_dir": "/public_html",
    "target_dir": "fsmw"
}

# O conteúdo do index.html (sem alterações)
INDEX_HTML_CONTENT = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Acessando FSMW...</title>
    <style>
        body { font-family: sans-serif; background-color: #121212; color: #e0e0e0; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .container { text-align: center; }
        .loader { border: 4px solid #f3f3f3; border-top: 4px solid #3498db; border-radius: 50%; width: 40px; height: 40px; animation: spin 2s linear infinite; margin: 0 auto 20px; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    </style>
</head>
<body>
    <div class="container">
        <div class="loader"></div>
        <p id="status">Conectando ao servidor de arquivos FSMW...</p>
    </div>
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            fetch('ngrok_fsmw.json', { cache: 'no-store' })
                .then(response => {
                    if (!response.ok) throw new Error('Falha ao carregar configuração');
                    return response.json();
                })
                .then(data => {
                    if (data && data.fsmw_url) {
                        document.getElementById('status').textContent = 'Redirecionando...';
                        window.location.href = data.fsmw_url;
                    } else {
                        throw new Error('URL do FSMW não encontrada no arquivo de configuração.');
                    }
                })
                .catch(error => {
                    console.error('Erro:', error);
                    document.getElementById('status').textContent = 'Erro ao conectar. O servidor pode estar offline.';
                });
        });
    </script>
</body>
</html>
"""

def provision_remote_server():
    print("--- 🚀 Provisionando Ponto de Acesso Remoto ---")
    
    if not all([FTP_CONFIG["host"], FTP_CONFIG["user"], FTP_CONFIG["password"]]):
        print("❌ ERRO: Credenciais FTP não foram carregadas. Verifique o arquivo .env e a função de leitura.")
        return

    ftp = None
    try:
        print(f"🔄 Conectando a {FTP_CONFIG['host']}...")
        ftp = FTP(FTP_CONFIG['host'], timeout=15)
        ftp.login(FTP_CONFIG['user'], FTP_CONFIG['password'])
        ftp.set_pasv(True)
        print("✅ Conexão FTP estabelecida com sucesso!")

        ftp.cwd(FTP_CONFIG['base_dir'])
        ftp.cwd(FTP_CONFIG['target_dir'])
        print(f"✅ Navegou para o diretório alvo: {FTP_CONFIG['base_dir']}/{FTP_CONFIG['target_dir']}")

        html_bytes = io.BytesIO(INDEX_HTML_CONTENT.encode('utf-8'))
        ftp.storbinary(f"STOR index.html", html_bytes)
        print(f"✅ Arquivo 'index.html' criado/atualizado com sucesso.")
        
        print("\n--- ✅ Provisionamento concluído! ---")

    except error_perm as e:
        print(f"❌ ERRO DE AUTENTICAÇÃO OU PERMISSÃO: {e}")
    except Exception as e:
        print(f"❌ ERRO INESPERADO durante o provisionamento via FTP: {e}")
    finally:
        if ftp:
            ftp.quit()

if __name__ == "__main__":
    provision_remote_server()

