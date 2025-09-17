
# ROTAS DE AUTENTICAÇÃO



# importações necessárias
from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from src.models.models import db, Usuario, LogsAcesso
from datetime import datetime

# Cria um blueprint (grupo de rotas) para autenticação
auth_bp = Blueprint('auth', __name__)


# ROTA: CADASTRAR USUÁRIO
# POST /api/auth/register

@auth_bp.route('/register', methods=['POST'])
def cadastrar_usuario():
    """
    Cadastra um novo usuário no sistema
    Recebe: nome, email, senha, perfil (opcional)
    Retorna: dados do usuário criado ou erro
    """
    try:
        # pega os dados enviados pelo cliente (JSON)
        dados = request.get_json()
        
        # verifica se foram enviados dados
        if not dados:
            return jsonify({'erro': 'Nenhum dado foi enviado'}), 400
        
        # extrai os campos necessários
        nome = dados.get('nome')
        email = dados.get('email')
        senha = dados.get('senha')
        perfil = dados.get('perfil', 'admin')  # Se não informar, será 'admin'
        
        # validações básicas
        if not nome or not email or not senha:
            return jsonify({'erro': 'Nome, email e senha são obrigatórios'}), 400
        
        if len(nome) > 80:
            return jsonify({'erro': 'Nome muito longo (máximo 80 caracteres)'}), 400
        
        if len(email) > 50:
            return jsonify({'erro': 'Email muito longo (máximo 50 caracteres)'}), 400
        
        if len(senha) < 6:
            return jsonify({'erro': 'Senha deve ter pelo menos 6 caracteres'}), 400
        
        # verifica se o email já está sendo usado
        usuario_existente = Usuario.query.filter_by(email=email).first()
        if usuario_existente:
            return jsonify({'erro': 'Este email já está cadastrado'}), 400
        
        # cria um novo usuário
        novo_usuario = Usuario(
            nome=nome,
            email=email,
            perfil=perfil
        )
        # criptografa e salva a senha
        novo_usuario.definir_senha(senha)
        
        # salva no banco de dados
        db.session.add(novo_usuario)
        db.session.commit()
        
        # registra a ação no log
        log = LogsAcesso(
            id_usuario=novo_usuario.id_usuario,
            acao='Usuário cadastrado no sistema',
            data_hora=datetime.utcnow()
        )
        db.session.add(log)
        db.session.commit()
        
        # retorna sucesso
        return jsonify({
            'mensagem': 'Usuário cadastrado com sucesso!',
            'usuario': novo_usuario.para_dict()
        }), 201
        
    except Exception as e:
        # se deu erro, desfaz as alterações no banco
        db.session.rollback()
        return jsonify({'erro': f'Erro no servidor: {str(e)}'}), 500

#  ROTA: FAZER LOGIN
#  POST /api/auth/login


@auth_bp.route('/login', methods=['POST'])
def fazer_login():
    """
    Faz login do usuário no sistema
    Recebe: email, senha
    Retorna: dados do usuário logado ou erro
    """
    try:
        # pega os dados enviados
        dados = request.get_json()
        
        if not dados:
            return jsonify({'erro': 'Nenhum dado foi enviado'}), 400
        
        email = dados.get('email')
        senha = dados.get('senha')
        
        # verifica se email e senha foram informados
        if not email or not senha:
            return jsonify({'erro': 'Email e senha são obrigatórios'}), 400
        
        # busca o usuário pelo email
        usuario = Usuario.query.filter_by(email=email).first()
        
        # Verifica se o usuário existe e se a senha está correta
        if not usuario or not usuario.verificar_senha(senha):
            return jsonify({'erro': 'Email ou senha incorretos'}), 401
        
        # faz o login (cria a sessão)
        login_user(usuario)
        
        # registra o login no log
        log = LogsAcesso(
            id_usuario=usuario.id_usuario,
            acao='Login realizado',
            data_hora=datetime.utcnow()
        )
        db.session.add(log)
        db.session.commit()
        
        # retorna sucesso
        return jsonify({
            'mensagem': 'Login realizado com sucesso!',
            'usuario': usuario.para_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': f'Erro no servidor: {str(e)}'}), 500

#  ROTA: FAZER LOGOUT
#  POST /api/auth/logout

@auth_bp.route('/logout', methods=['POST'])
@login_required  # só funciona se o usuário estiver logado
def fazer_logout():
    """
    Faz logout do usuário (encerra a sessão)
    """
    try:
        # registra o logout no log antes de sair
        log = LogsAcesso(
            id_usuario=current_user.id_usuario,
            acao='Logout realizado',
            data_hora=datetime.utcnow()
        )
        db.session.add(log)
        db.session.commit()
        
        # faz o logout (encerra a sessão)
        logout_user()
        
        return jsonify({'mensagem': 'Logout realizado com sucesso!'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': f'Erro no servidor: {str(e)}'}), 500


#  ROTA: VERIFICAR SE ESTÁ LOGADO
#  GET /api/auth/verificar


@auth_bp.route('/verificar', methods=['GET'])
def verificar_login():
    """
    Verifica se o usuário está logado
    Retorna: dados do usuário se logado, ou status de não logado
    """
    try:
        if current_user.is_authenticated:
            # usuário está logado
            return jsonify({
                'logado': True,
                'usuario': current_user.para_dict()
            }), 200
        else:
            # usuário não está logado
            return jsonify({'logado': False}), 200
            
    except Exception as e:
        return jsonify({'erro': f'Erro no servidor: {str(e)}'}), 500

