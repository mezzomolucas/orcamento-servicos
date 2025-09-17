
# MODELO DO BANCO DE DADOS


# importações necessárias
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Inicializa o banco de dados
db = SQLAlchemy()

# MODELO: USUÁRIO

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuario'
    
    # campos da tabela
    id_usuario = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)      
    email = db.Column(db.String(50), unique=True, nullable=False)  
    senha = db.Column(db.String(40), nullable=False)     
    perfil = db.Column(db.String(18), default='admin')    
    
    # relacionamentos (um usuário pode ter vários orçamentos e logs)
    orcamentos = db.relationship('Orcamento', backref='usuario', lazy=True)
    logs = db.relationship('LogsAcesso', backref='usuario', lazy=True)
    
    # método obrigatório para o Flask-Login funcionar
    def get_id(self):
        return str(self.id_usuario)
    
    # criptografa e salva a senha
    def definir_senha(self, senha):
        self.senha = generate_password_hash(senha)
    
    # verifica se a senha digitada está correta
    def verificar_senha(self, senha):
        return check_password_hash(self.senha, senha)
    
    #  onverte o usuário para formato JSON (para APIs)
    def para_dict(self):
        return {
            'id_usuario': self.id_usuario,
            'nome': self.nome,
            'email': self.email,
            'perfil': self.perfil
        }

# MODELO: CLIENTE

class Cliente(db.Model):
    __tablename__ = 'clientes'
    
    # campos da tabela
    id_cliente = db.Column(db.Integer, primary_key=True) 
    nome = db.Column(db.String(80), nullable=False)     
    telefone = db.Column(db.String(11))           
    email = db.Column(db.String(50))               
    endereco = db.Column(db.String(55))
    
    # relacionamento (um cliente pode ter vários orçamentos)
    orcamentos = db.relationship('Orcamento', backref='cliente', lazy=True)
    
    # converte o cliente para formato JSON
    def para_dict(self):
        return {
            'id_cliente': self.id_cliente,
            'nome': self.nome,
            'telefone': self.telefone,
            'email': self.email,
            'endereco': self.endereco
        }

# MODELO: SERVIÇO


class Servico(db.Model):
    __tablename__ = 'servicos'
    
    # campos da tabela
    id_servicos = db.Column(db.Integer, primary_key=True) 
    nome = db.Column(db.String(80), nullable=False)    
    descricao = db.Column(db.String(255))                
    valor = db.Column(db.Numeric(10, 2), nullable=False)  
    
    # relacionamento (um serviço pode estar em vários orçamentos)
    orcamento_servicos = db.relationship('OrcamentoServicos', backref='servico', lazy=True)
    
    # converte o serviço para formato JSON
    def para_dict(self):
        return {
            'id_servicos': self.id_servicos,
            'nome': self.nome,
            'descricao': self.descricao,
            'valor': float(self.valor)  #
        }

# MODELO: ORÇAMENTO


class Orcamento(db.Model):
    __tablename__ = 'orcamento'
    
    # campos da tabela
    id_orcamento = db.Column(db.Integer, primary_key=True) 
    id_cliente = db.Column(db.Integer, db.ForeignKey('clientes.id_cliente'), nullable=False) 
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=False)   
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)  
    valor_total = db.Column(db.Numeric(10, 2), nullable=False)     
    
    # relacionamento (um orçamento pode ter vários serviços)
    orcamento_servicos = db.relationship('OrcamentoServicos', backref='orcamento', lazy=True, cascade='all, delete-orphan')
    
    # converte o orçamento para formato JSON
    def para_dict(self):
        return {
            'id_orcamento': self.id_orcamento,
            'id_cliente': self.id_cliente,
            'id_usuario': self.id_usuario,
            'data_criacao': self.data_criacao.isoformat() if self.data_criacao else None,
            'valor_total': float(self.valor_total),
            'cliente_nome': self.cliente.nome if self.cliente else None,
            'usuario_nome': self.usuario.nome if self.usuario else None
        }

# MODELO: ORÇAMENTO_SERVIÇOS


class OrcamentoServicos(db.Model):
    __tablename__ = 'orcamento_servicos'
    
    # chaves primárias compostas
    id_orcamento = db.Column(db.Integer, db.ForeignKey('orcamento.id_orcamento'), primary_key=True)
    id_servico = db.Column(db.Integer, db.ForeignKey('servicos.id_servicos'), primary_key=True)
    
    # campos adicionais
    quantidade = db.Column(db.Integer, default=1)                    
    valor_unitario = db.Column(db.Numeric(10, 2), nullable=False)    
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)         
    
    # converte para formato JSON
    def para_dict(self):
        return {
            'id_orcamento': self.id_orcamento,
            'id_servico': self.id_servico,
            'quantidade': self.quantidade,
            'valor_unitario': float(self.valor_unitario),
            'subtotal': float(self.subtotal),
            'servico_nome': self.servico.nome if self.servico else None,
            'servico_descricao': self.servico.descricao if self.servico else None
        }


#  MODELO: LOGS DE ACESSO

class LogsAcesso(db.Model):
    __tablename__ = 'logs_acesso'
    
    # Campos da tabela
    id_log = db.Column(db.Integer, primary_key=True)     
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=False) 
    acao = db.Column(db.String(100), nullable=False)    
    data_hora = db.Column(db.DateTime, default=datetime.utcnow)  
    
    # converte para formato JSON
    def para_dict(self):
        return {
            'id_log': self.id_log,
            'id_usuario': self.id_usuario,
            'acao': self.acao,
            'data_hora': self.data_hora.isoformat() if self.data_hora else None,
            'usuario_nome': self.usuario.nome if self.usuario else None
        }

