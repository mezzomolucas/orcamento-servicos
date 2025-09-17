<<<<<<< HEAD
# 📖 Guia de Uso - Sistema de Orçamentos

## 🎯 Para os Colegas do Grupo

Este guia foi criado para ajudar vocês a entenderem e usarem o sistema que desenvolvemos para o Sprint 2.

## 🚀 Como Executar o Sistema

### 1. Abrir o Terminal
```bash
# Navegar para a pasta do projeto
cd orcamentos_servicos

# Ativar o ambiente virtual
source venv/bin/activate

# Executar o sistema (versão simplificada)
python src/main_simples.py
```

### 2. Acessar o Sistema
- Abra o navegador em: `http://localhost:5000`
- O sistema estará rodando e pronto para uso

## 📁 Arquivos Importantes

### 🔧 Arquivos Principais
- `src/main_simples.py` - **Arquivo principal** (mais fácil de entender)
- `src/main.py` - Arquivo principal original (mais complexo)

### 🗄️ Modelos do Banco
- `src/models/models_simples.py` - **Modelos comentados** (recomendado para estudo)
- `src/models/models.py` - Modelos originais

### 🛣️ Rotas (APIs)
- `src/routes/auth_simples.py` - **Login/Register comentado**
- `src/routes/clientes_simples.py` - **CRUD de Clientes comentado**
- `src/routes/servicos_simples.py` - **CRUD de Serviços comentado**

### 📚 Documentação
- `README.md` - Documentação completa do projeto
- `TESTES_REALIZADOS.md` - Relatório dos testes feitos
- `GUIA_DE_USO.md` - Este arquivo

## 🧪 Como Testar as Funcionalidades

### Usando o Terminal (curl)

#### 1. Cadastrar Usuário
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Seu Nome",
    "email": "seu@email.com",
    "senha": "123456"
  }'
```

#### 2. Fazer Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{
    "email": "seu@email.com",
    "senha": "123456"
  }'
```

#### 3. Cadastrar Cliente
```bash
curl -X POST 

,,3

3,3211  \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "nome": "João Silva",
    "telefone": "11999999999",
    "email": "joao@email.com",
    "endereco": "Rua A, 123"
  }'
```

#### 4. Listar Clientes
```bash
curl -X GET http://localhost:5000/api/clientes/ \
  -H "Content-Type: application/json" \
  -b cookies.txt
```

### Usando Postman ou Insomnia

1. **Importe as rotas**:
   - POST `/api/auth/register` - Cadastrar usuário
   - POST `/api/auth/login` - Fazer login
   - GET `/api/clientes/` - Listar clientes
   - POST `/api/clientes/` - Cadastrar cliente
   - GET `/api/servicos/` - Listar serviços
   - POST `/api/servicos/` - Cadastrar serviço

2. **Configure os headers**:
   - `Content-Type: application/json`

3. **Mantenha os cookies** para manter a sessão ativa

## 🔍 Entendendo o Código

### Estrutura Básica

```python
# 1. Importações
from flask import Flask, request, jsonify
from flask_login import login_required, current_user

# 2. Criar rota
@app.route('/api/clientes/', methods=['POST'])
@login_required  # Só funciona se estiver logado
def cadastrar_cliente():
    # 3. Pegar dados enviados
    dados = request.get_json()
    
    # 4. Validar dados
    if not dados.get('nome'):
        return jsonify({'erro': 'Nome é obrigatório'}), 400
    
    # 5. Salvar no banco
    cliente = Cliente(nome=dados['nome'])
    db.session.add(cliente)
    db.session.commit()
    
    # 6. Retornar resposta
    return jsonify({'mensagem': 'Cliente cadastrado!'}), 201
```

### Principais Conceitos

#### 🔐 Autenticação
- `@login_required` - Só permite acesso se estiver logado
- `current_user` - Usuário que está logado no momento
- `login_user()` - Faz login do usuário
- `logout_user()` - Faz logout do usuário

#### 🗄️ Banco de Dados
- `db.session.add()` - Adiciona novo registro
- `db.session.commit()` - Salva as alterações
- `db.session.rollback()` - Desfaz alterações em caso de erro
- `Model.query.all()` - Busca todos os registros
- `Model.query.get()` - Busca por ID

#### 🌐 APIs REST
- `GET` - Buscar/Listar dados
- `POST` - Criar novos dados
- `PUT` - Atualizar dados existentes
- `DELETE` - Excluir dados

## 🛠️ Modificando o Sistema

### Para Adicionar uma Nova Rota

1. **Abra o arquivo de rotas** (ex: `clientes_simples.py`)

2. **Adicione a nova função**:
```python
@clientes_bp.route('/buscar/<nome>', methods=['GET'])
@login_required
def buscar_por_nome(nome):
    clientes = Cliente.query.filter(Cliente.nome.contains(nome)).all()
    return jsonify({
        'clientes': [c.para_dict() for c in clientes]
    })
```

3. **Teste a nova rota**:
```bash
curl http://localhost:5000/api/clientes/buscar/Maria -b cookies.txt
```

### Para Adicionar um Novo Campo

1. **Modifique o modelo** (`models_simples.py`):
```python
class Cliente(db.Model):
    # ... campos existentes ...
    cpf = db.Column(db.String(11))  # Novo campo
```

2. **Atualize as rotas** para aceitar o novo campo

3. **Recrie o banco** (apague o arquivo `app.db` e execute novamente)

## ❗ Problemas Comuns

### "Erro 401 - Unauthorized"
- **Causa**: Não está logado
- **Solução**: Faça login primeiro e use os cookies

### "Erro 404 - Not Found"
- **Causa**: URL errada ou servidor não está rodando
- **Solução**: Verifique a URL e se o servidor está ativo

### "Erro 400 - Bad Request"
- **Causa**: Dados inválidos ou campos obrigatórios faltando
- **Solução**: Verifique os dados enviados

### Banco de dados não funciona
- **Solução**: Apague o arquivo `src/database/app.db` e execute novamente

## 📞 Dúvidas?

Se tiverem dúvidas sobre o código:

1. **Leiam os comentários** nos arquivos `*_simples.py`
2. **Consultem este guia** e o `README.md`
3. **Testem as APIs** usando curl ou Postman
4. **Perguntem no grupo** - estamos aqui para ajudar!

## 🎯 Próximos Passos

Para os próximos sprints, podemos implementar:
- Interface web (HTML/CSS/JavaScript)
- Geração de PDF dos orçamentos
- Envio de emails
- Relatórios e gráficos

**Boa sorte com o projeto! 🚀**

=======
🚀 Como Rodar e Testar no Postman
1. Executar o Sistema

No terminal:

cd orcamentos_servicos
source venv/bin/activate
python src/main.py


O servidor vai rodar em:
👉 http://localhost:5000

2. Testando com Postman
Usuários

Cadastrar Usuário
POST http://localhost:5000/api/auth/register

{
  "nome": "Seu Nome",
  "email": "seu@email.com",
  "senha": "123456"
}


Login
POST http://localhost:5000/api/auth/login

{
  "email": "seu@email.com",
  "senha": "123456"
}


🔑 O login gera a sessão (cookies).

Clientes

Cadastrar Cliente
POST http://localhost:5000/api/clientes/

{
  "nome": "João Silva",
  "telefone": "11999999999",
  "email": "joao@email.com",
  "endereco": "Rua A, 123"
}


Listar Clientes
GET http://localhost:5000/api/clientes/

Serviços

Cadastrar Serviço
POST http://localhost:5000/api/servicos/

{
  "descricao": "Dedetização",
  "valor": 500
}


Listar Serviços
GET http://localhost:5000/api/servicos/
>>>>>>> 0f4a9750a24800f21f4e2de2987bd62302ba3946
