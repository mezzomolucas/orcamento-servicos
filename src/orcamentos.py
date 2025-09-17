from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from src.models.models import db, Orcamento, OrcamentoServicos, Cliente, Servico, LogsAcesso
from datetime import datetime
from decimal import Decimal

orcamentos_bp = Blueprint('orcamentos', __name__)

@orcamentos_bp.route('/', methods=['GET'])
@login_required
def get_orcamentos():
    try:
        orcamentos = Orcamento.query.all()
        orcamentos_data = []
        
        for orcamento in orcamentos:
            orcamento_dict = orcamento.to_dict()
            # Adicionar serviços do orçamento
            servicos = []
            for os in orcamento.orcamento_servicos:
                servicos.append(os.to_dict())
            orcamento_dict['servicos'] = servicos
            orcamentos_data.append(orcamento_dict)
        
        return jsonify({
            'orcamentos': orcamentos_data
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Erro interno do servidor: {str(e)}'}), 500

@orcamentos_bp.route('/<int:id_orcamento>', methods=['GET'])
@login_required
def get_orcamento(id_orcamento):
    try:
        orcamento = Orcamento.query.get_or_404(id_orcamento)
        orcamento_dict = orcamento.to_dict()
        
        # Adicionar serviços do orçamento
        servicos = []
        for os in orcamento.orcamento_servicos:
            servicos.append(os.to_dict())
        orcamento_dict['servicos'] = servicos
        
        return jsonify({
            'orcamento': orcamento_dict
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Erro interno do servidor: {str(e)}'}), 500

@orcamentos_bp.route('/', methods=['POST'])
@login_required
def create_orcamento():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Dados não fornecidos'}), 400
        
        id_cliente = data.get('id_cliente')
        servicos = data.get('servicos', [])
        
        # Validações básicas
        if not id_cliente:
            return jsonify({'error': 'ID do cliente é obrigatório'}), 400
        
        if not servicos:
            return jsonify({'error': 'Pelo menos um serviço deve ser selecionado'}), 400
        
        # Verificar se o cliente existe
        cliente = Cliente.query.get(id_cliente)
        if not cliente:
            return jsonify({'error': 'Cliente não encontrado'}), 404
        
        # Calcular valor total
        valor_total = Decimal('0')
        servicos_validados = []
        
        for servico_data in servicos:
            id_servico = servico_data.get('id_servico')
            quantidade = servico_data.get('quantidade', 1)
            
            if not id_servico:
                return jsonify({'error': 'ID do serviço é obrigatório'}), 400
            
            servico = Servico.query.get(id_servico)
            if not servico:
                return jsonify({'error': f'Serviço com ID {id_servico} não encontrado'}), 404
            
            try:
                quantidade = int(quantidade)
                if quantidade <= 0:
                    return jsonify({'error': 'Quantidade deve ser maior que zero'}), 400
            except (ValueError, TypeError):
                return jsonify({'error': 'Quantidade deve ser um número inteiro válido'}), 400
            
            valor_unitario = servico.valor
            subtotal = valor_unitario * quantidade
            valor_total += subtotal
            
            servicos_validados.append({
                'id_servico': id_servico,
                'quantidade': quantidade,
                'valor_unitario': valor_unitario,
                'subtotal': subtotal
            })
        
        # Criar novo orçamento
        new_orcamento = Orcamento(
            id_cliente=id_cliente,
            id_usuario=current_user.id_usuario,
            data_criacao=datetime.utcnow(),
            valor_total=valor_total
        )
        
        db.session.add(new_orcamento)
        db.session.flush()  # Para obter o ID do orçamento
        
        # Criar registros de orçamento_servicos
        for servico_data in servicos_validados:
            orcamento_servico = OrcamentoServicos(
                id_orcamento=new_orcamento.id_orcamento,
                id_servico=servico_data['id_servico'],
                quantidade=servico_data['quantidade'],
                valor_unitario=servico_data['valor_unitario'],
                subtotal=servico_data['subtotal']
            )
            db.session.add(orcamento_servico)
        
        db.session.commit()
        
        # Log da ação
        log = LogsAcesso(
            id_usuario=current_user.id_usuario,
            acao=f'Orçamento criado para cliente: {cliente.nome}',
            data_hora=datetime.utcnow()
        )
        db.session.add(log)
        db.session.commit()
        
        # Retornar orçamento completo
        orcamento_dict = new_orcamento.to_dict()
        servicos_response = []
        for os in new_orcamento.orcamento_servicos:
            servicos_response.append(os.to_dict())
        orcamento_dict['servicos'] = servicos_response
        
        return jsonify({
            'message': 'Orçamento criado com sucesso',
            'orcamento': orcamento_dict
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro interno do servidor: {str(e)}'}), 500

@orcamentos_bp.route('/<int:id_orcamento>', methods=['PUT'])
@login_required
def update_orcamento(id_orcamento):
    try:
        orcamento = Orcamento.query.get_or_404(id_orcamento)
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Dados não fornecidos'}), 400
        
        id_cliente = data.get('id_cliente')
        servicos = data.get('servicos')
        
        # Atualizar cliente se fornecido
        if id_cliente is not None:
            cliente = Cliente.query.get(id_cliente)
            if not cliente:
                return jsonify({'error': 'Cliente não encontrado'}), 404
            orcamento.id_cliente = id_cliente
        
        # Atualizar serviços se fornecidos
        if servicos is not None:
            if not servicos:
                return jsonify({'error': 'Pelo menos um serviço deve ser selecionado'}), 400
            
            # Remover serviços existentes
            OrcamentoServicos.query.filter_by(id_orcamento=id_orcamento).delete()
            
            # Calcular novo valor total
            valor_total = Decimal('0')
            servicos_validados = []
            
            for servico_data in servicos:
                id_servico = servico_data.get('id_servico')
                quantidade = servico_data.get('quantidade', 1)
                
                if not id_servico:
                    return jsonify({'error': 'ID do serviço é obrigatório'}), 400
                
                servico = Servico.query.get(id_servico)
                if not servico:
                    return jsonify({'error': f'Serviço com ID {id_servico} não encontrado'}), 404
                
                try:
                    quantidade = int(quantidade)
                    if quantidade <= 0:
                        return jsonify({'error': 'Quantidade deve ser maior que zero'}), 400
                except (ValueError, TypeError):
                    return jsonify({'error': 'Quantidade deve ser um número inteiro válido'}), 400
                
                valor_unitario = servico.valor
                subtotal = valor_unitario * quantidade
                valor_total += subtotal
                
                servicos_validados.append({
                    'id_servico': id_servico,
                    'quantidade': quantidade,
                    'valor_unitario': valor_unitario,
                    'subtotal': subtotal
                })
            
            # Criar novos registros de orçamento_servicos
            for servico_data in servicos_validados:
                orcamento_servico = OrcamentoServicos(
                    id_orcamento=id_orcamento,
                    id_servico=servico_data['id_servico'],
                    quantidade=servico_data['quantidade'],
                    valor_unitario=servico_data['valor_unitario'],
                    subtotal=servico_data['subtotal']
                )
                db.session.add(orcamento_servico)
            
            orcamento.valor_total = valor_total
        
        db.session.commit()
        
        # Log da ação
        log = LogsAcesso(
            id_usuario=current_user.id_usuario,
            acao=f'Orçamento atualizado: {id_orcamento}',
            data_hora=datetime.utcnow()
        )
        db.session.add(log)
        db.session.commit()
        
        # Retornar orçamento completo
        orcamento_dict = orcamento.to_dict()
        servicos_response = []
        for os in orcamento.orcamento_servicos:
            servicos_response.append(os.to_dict())
        orcamento_dict['servicos'] = servicos_response
        
        return jsonify({
            'message': 'Orçamento atualizado com sucesso',
            'orcamento': orcamento_dict
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro interno do servidor: {str(e)}'}), 500

@orcamentos_bp.route('/<int:id_orcamento>', methods=['DELETE'])
@login_required
def delete_orcamento(id_orcamento):
    try:
        orcamento = Orcamento.query.get_or_404(id_orcamento)
        
        # Os registros de OrcamentoServicos serão deletados automaticamente devido ao cascade
        db.session.delete(orcamento)
        db.session.commit()
        
        # Log da ação
        log = LogsAcesso(
            id_usuario=current_user.id_usuario,
            acao=f'Orçamento excluído: {id_orcamento}',
            data_hora=datetime.utcnow()
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify({
            'message': 'Orçamento excluído com sucesso'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro interno do servidor: {str(e)}'}), 500

