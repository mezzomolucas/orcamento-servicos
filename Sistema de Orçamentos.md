# 🏢 Sistema de Orçamentos de Serviços

Sistema desenvolvido para facilitar a criação e gerenciamento de orçamentos de uma empresa de serviços.

## 📋 Funcionalidades

### ✅ Implementadas no Sprint 2
- **Autenticação**: Login e cadastro de usuários
- **CRUD de Clientes**: Cadastrar, listar, editar e excluir clientes
- **CRUD de Serviços**: Cadastrar, listar, editar e excluir serviços
- **CRUD de Orçamentos**: Criar, listar, editar e excluir orçamentos
- **Logs de Acesso**: Registro de todas as ações dos usuários

### 🔄 Para Próximos Sprints
- Interface web (frontend)
- Geração de PDF dos orçamentos
- Envio de orçamentos por email
- Relatórios e estatísticas

## 🗂️ Estrutura do Projeto

```
orcamentos_servicos/
├── src/
│   ├── models/
│   │   ├── models.py          # Modelos originais (mais complexos)
│   │   └── models_simples.py  # Modelos simplificados e comentados
│   ├── routes/
│   │   ├── auth.py            # Rotas de autenticação originais
│   │   ├── auth_simples.py    # Rotas de autenticação simplificadas
│   │   ├── clientes.py        # CRUD de clientes original
│   │   ├── clientes_simples.py # CRUD de clientes simplificado
│   │   ├── servicos.py        # CRUD de serviços original
│   │   └── servicos_simples.py # CRUD de serviços simplificado
│   ├── static/                # Arquivos estáticos (HTML, CSS, JS)
│   ├── database/
│   │   └── app.db            # Banco de dados SQLite
│   ├── main.py               # Arquivo principal original
│   └── main_simples.py       # Arquivo principal simplificado
├── venv/                     # Ambiente virtual Python
├── requirements.txt          # Dependências do projeto
└── README.md                # Este arquivo
```

## 🚀 Como Executar

### 1. Ativar o ambiente virtual
```bash
cd orcamentos_servicos
source venv/bin/activate
```

### 2. Instalar dependências (se necessário)
```bash
pip install -r requirements.txt
```

### 3. Executar o sistema
```bash
# Versão simplificada (recomendada para estudo)
python src/main_simples.py

# OU versão original
python src/main.py
```

### 4. Acessar o sistema
- Abra o navegador em: `http://localhost:5000`
- Para testar as APIs, use um cliente REST como Postman ou Insomnia

## 📡 APIs Disponíveis

### 🔐 Autenticação
- `POST /api/auth/register` - Cadastrar usuário
- `POST /api/auth/login` - Fazer login
- `POST /api/auth/logout` - Fazer logout
- `GET /api/auth/verificar` - Verificar se está logado

### 👥 Clientes
- `GET /api/clientes/` - Listar todos os clientes
- `GET /api/clientes/<id>` - Buscar cliente específico
- `POST /api/clientes/` - Cadastrar novo cliente
- `PUT /api/clientes/<id>` - Atualizar cliente
- `DELETE /api/clientes/<id>` - Excluir cliente

### 🛠️ Serviços
- `GET /api/servicos/` - Listar todos os serviços
- `GET /api/servicos/<id>` - Buscar serviço específico
- `POST /api/servicos/` - Cadastrar novo serviço
- `PUT /api/servicos/<id>` - Atualizar serviço
- `DELETE /api/servicos/<id>` - Excluir serviço

## 🗄️ Banco de Dados

O sistema usa SQLite com as seguintes tabelas:

- **usuario**: Usuários do sistema
- **clientes**: Clientes da empresa
- **servicos**: Serviços oferecidos
- **orcamento**: Orçamentos criados
- **orcamento_servicos**: Relação entre orçamentos e serviços
- **logs_acesso**: Log de ações dos usuários

## 🧪 Como Testar

### 1. Cadastrar um usuário
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "João Silva",
    "email": "joao@email.com",
    "senha": "123456"
  }'
```

### 2. Fazer login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "joao@email.com",
    "senha": "123456"
  }'
```

### 3. Cadastrar um cliente (após login)
```bash
curl -X POST http://localhost:5000/api/clientes/ \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Maria Santos",
    "telefone": "11999999999",
    "email": "maria@email.com",
    "endereco": "Rua das Flores, 123"
  }'
```

## 👥 Equipe de Desenvolvimento

- Roberto E. Henz
- Hérick G. Pereira  
- Arthur Primaz
- Lucas Mezzomo

## 📝 Observações

- Os arquivos com sufixo `_simples.py` são versões comentadas e mais fáceis de entender
- O sistema está configurado para desenvolvimento (debug=True)
- Em produção, lembre-se de alterar a SECRET_KEY
- O banco de dados é criado automaticamente na primeira execução

