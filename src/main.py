# ========================================
# ARQUIVO PRINCIPAL DO SISTEMA
# Sistema de Orçamentos de Serviços
# ========================================

import os
import sys

# Configuração necessária para importar os módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Importações do Flask e extensões
from flask import Flask, send_from_directory
from flask_login import LoginManager

# Importações dos nossos módulos
from src.models.models import db, Usuario
from src.routes.auth import auth_bp
from src.routes.clientes import clientes_bp
from src.routes.servicos import servicos_bp

# ========================================
# CONFIGURAÇÃO DO FLASK
# ========================================

# Cria a aplicação Flask
app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))

# Chave secreta para sessões (IMPORTANTE: mude em produção!)
app.config['SECRET_KEY'] = 'sua-chave-secreta-aqui-mude-em-producao'

# ========================================
# CONFIGURAÇÃO DO LOGIN
# ========================================

# Inicializa o gerenciador de login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.fazer_login'  # Rota para login
login_manager.login_message = 'Você precisa fazer login para acessar esta página.'

# Função que carrega o usuário pela sessão
@login_manager.user_loader
def carregar_usuario(id_usuario):
    """
    Função obrigatória do Flask-Login
    Carrega o usuário pelo ID armazenado na sessão
    """
    return Usuario.query.get(int(id_usuario))

# ========================================
# REGISTRO DAS ROTAS
# ========================================

# Registra os grupos de rotas (blueprints)
app.register_blueprint(auth_bp, url_prefix='/api/auth')        # Rotas de login/logout
app.register_blueprint(clientes_bp, url_prefix='/api/clientes') # Rotas de clientes
app.register_blueprint(servicos_bp, url_prefix='/api/servicos') # Rotas de serviços

# ========================================
# CONFIGURAÇÃO DO BANCO DE DADOS
# ========================================

# Caminho para o arquivo do banco SQLite
caminho_banco = os.path.join(os.path.dirname(__file__), 'database', 'app.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{caminho_banco}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desabilita avisos desnecessários

# Inicializa o banco de dados
db.init_app(app)

# Cria as tabelas se não existirem
with app.app_context():
    db.create_all()
    print("✅ Banco de dados inicializado!")

# ========================================
# ROTAS PARA SERVIR ARQUIVOS ESTÁTICOS
# ========================================

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def servir_arquivos(path):
    """
    Serve os arquivos estáticos (HTML, CSS, JS)
    Se não encontrar o arquivo, serve o index.html (para SPAs)
    """
    pasta_estaticos = app.static_folder
    
    if pasta_estaticos is None:
        return "Pasta de arquivos estáticos não configurada", 404

    # Se o arquivo existe, serve ele
    if path != "" and os.path.exists(os.path.join(pasta_estaticos, path)):
        return send_from_directory(pasta_estaticos, path)
    else:
        # Se não existe, tenta servir o index.html
        index_path = os.path.join(pasta_estaticos, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(pasta_estaticos, 'index.html')
        else:
            return "Arquivo index.html não encontrado", 404

# ========================================
# INICIALIZAÇÃO DO SERVIDOR
# ========================================

if __name__ == '__main__':
    print("🚀 Iniciando o Sistema de Orçamentos de Serviços...")
    print("📍 Acesse: http://localhost:5000")
    print("🛑 Para parar: Ctrl+C")
    
    # Inicia o servidor Flask
    # host='0.0.0.0' permite acesso de outros computadores na rede
    # debug=True reinicia automaticamente quando o código muda
    app.run(host='0.0.0.0', port=5000, debug=True)

